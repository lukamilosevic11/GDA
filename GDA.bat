::
:: GDA Copyright (c) 2022.
:: University of Belgrade, Faculty of Mathematics
:: Luka Milosevic
:: lukamilosevic11@gmail.com
::
:: Permission is hereby granted, free of charge, to any person obtaining a copy
:: of this software and associated documentation files (the "Software"), to deal
:: in the Software without restriction, including without limitation the rights
:: to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
:: copies of the Software, and to permit persons to whom the Software is
:: furnished to do so, subject to the following conditions:
::
:: The above copyright notice and this permission notice shall be included in
:: all copies or substantial portions of the Software.
::

@echo off

SET /A ARGS_NUM=0
FOR %%x IN (%*) DO SET /A ARGS_NUM+=1

IF %ARGS_NUM% EQU 0 (
	CALL :Help %~0 1
	GOTO :eof
)

for /f %%i in ('
  powershell [guid]::NewGuid(^).ToString(^)
') do set API_KEY=%%i	

IF %~1==-h (
	CALL :Help %~0 0
	GOTO :eof
)

IF %~1==-help (
	CALL :Help %~0 0
	GOTO :eof
)

IF %~1==-s (
	GOTO :Start
	GOTO :eof
)

IF %~1==-start (
	GOTO :Start
	GOTO :eof
)

IF %~1==-e (
	GOTO :Exit
	GOTO :eof
)

IF %~1==-exit (
	GOTO :Exit
	GOTO :eof
)

IF %~1==-u (
	IF %ARGS_NUM% GEQ 2 (
		CALL :UpOutput %~2
		GOTO :eof
	) ELSE (
		GOTO :Up
		GOTO :eof
	)
)

IF %~1==-up (
	IF %ARGS_NUM% GEQ 2 (
		CALL :UpOutput %~2
		GOTO :eof
	) ELSE (
		GOTO :Up
		GOTO :eof
	)
)

IF %~1==-d (
    IF %ARGS_NUM% GEQ 2 (
		CALL :DownReset %~2
		GOTO :eof
	) ELSE (
        GOTO :Down
        GOTO :eof
	)
)

IF %~1==-down (
    IF %ARGS_NUM% GEQ 2 (
		CALL :DownReset %~2
		GOTO :eof
	) ELSE (
        GOTO :Down
        GOTO :eof
	)
)


CALL :Help %~0 1
GOTO :eof

:Start
	docker-compose -f gda-compose.yml -p gene-disease-annotation start
	GOTO :eof

:Exit
	docker-compose -f gda-compose.yml -p gene-disease-annotation stop
	GOTO :eof

:Up
	docker-compose -f gda-compose.yml -p gene-disease-annotation up -d
	GOTO :eof
	
:UpOutput
	IF "%~1" == "-o" (
		docker-compose -f gda-compose.yml -p gene-disease-annotation up
		GOTO :eof
	)
	
	IF "%~1" == "-output" (
		docker-compose -f gda-compose.yml -p gene-disease-annotation up
		GOTO :eof
	)

	GOTO :Up
	GOTO :eof

:Down
	docker-compose -f gda-compose.yml -p gene-disease-annotation down
	GOTO :eof

:DownReset
    IF "%~1" == "-r" (
		docker-compose -f gda-compose.yml -p gene-disease-annotation down --rmi all -v --remove-orphans
		GOTO :eof
	)

	IF "%~1" == "-reset" (
		docker-compose -f gda-compose.yml -p gene-disease-annotation down --rmi all -v --remove-orphans
		GOTO :eof
	)

	GOTO :Down
	GOTO :eof

:Help
	ECHO.
	IF "%~2" == "1" (
		ECHO Wrong argument, see usage below!
		ECHO.
	)
	ECHO Usage: %~1 ^<options^> [output mode]
	ECHO   -h^|-help           Shows this help text.
	ECHO   -s^|-start          Starts existing containers for a service.
	ECHO                      Starts the stopped containers, can't create new ones.
	ECHO                      Can be run only in detach mode. There is no output.
	ECHO   -e^|-exit           Exits/Stops running containers without removing them.
	ECHO                      They can be started again with start command.
	ECHO   -u^|-up             Builds, (re)creates, and starts containers.
	ECHO                      Run in detached mode or in the background. There is no output.
	ECHO   -u^|-up -o^|-output  Shows output of execution for Typesense and GDA.
	ECHO   -d^|-down           Stops containers and by default, the only things removed are:
	ECHO                        - Containers for services defined in the gda-compose file
	ECHO                        - Networks defined in the networks section of the gda-compose file
	ECHO                        - The default network, if one is used
	ECHO                      Networks and volumes defined as external are never removed.
	ECHO   -d^|-down -r^|-reset Stops containers and removes containers, networks, volumes, and images created by up command.
	GOTO :eof