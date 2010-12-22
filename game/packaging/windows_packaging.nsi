!define PRODUCT_NAME "PARPG Techdemo 1"
!define PRODUCT_VERSION "SVN trunk r522"
!define PRODUCT_PUBLISHER "PARPG Development Team"
!define PRODUCT_WEB_SITE "http://www.parpg.net/"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PARPG_DIR ".."

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${PARPG_DIR}\gui\icons\window_icon.ico"
!define MUI_UNICON "${PARPG_DIR}\gui\icons\window_icon.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME

!insertmacro MUI_PAGE_COMPONENTS

; License page
!insertmacro MUI_PAGE_LICENSE "${PARPG_DIR}\license\gpl30.license"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\game\README.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

RequestExecutionLevel admin ;For Vista. Admin is needed to install in program files directory

Name "${PRODUCT_NAME}"
OutFile "parpg_td1_r522_win32.exe"
InstallDir "$PROGRAMFILES\PARPG"
ShowInstDetails show
ShowUnInstDetails show

;------------ Main. Packages PARPG code --------------
Section "PARPG" PARPG
  SectionIn RO
  SetOutPath "$INSTDIR\game"
  SetOverwrite try
  
  ;Get all the core PARPG files
  FILE /r "${PARPG_DIR}\*.ttf"
  FILE /r "${PARPG_DIR}\*.py"
  FILE /r "${PARPG_DIR}\*.yaml"
  FILE /r /x "settings.xml" "${PARPG_DIR}\*.xml"
  FILE /r "${PARPG_DIR}\*.png"
  FILE /r "${PARPG_DIR}\*.ico"
  FILE /r "${PARPG_DIR}\*.ogg"
  FILE /r "${PARPG_DIR}\*.license"
  
  FILE "${PARPG_DIR}\README"
  FILE "${PARPG_DIR}\log_parpg.bat"

  RENAME "settings-dist.xml" "settings.xml"
  RENAME "README" "README.txt"
  
  CreateDirectory "$INSTDIR\game\saves"  
  
  SetAutoClose true
SectionEnd

Section -Tools
  SetOutPath "$INSTDIR\tools\map_editor"
  SetOverwrite try
  
  FILE /r "${PARPG_DIR}\..\tools\map_editor\*.ttf"
  FILE /r "${PARPG_DIR}\..\tools\map_editor\*.py"
  FILE /r /x "settings.xml" "${PARPG_DIR}\..\tools\map_editor\*.xml"
  FILE /r "${PARPG_DIR}\..\tools\map_editor\*.png"
  FILE /r "${PARPG_DIR}\..\tools\map_editor\*.txt"
  RENAME "settings-dist.xml" "settings.xml"
  
SectionEnd

Section -AdditionalIcons
  ;avoid shortcuts headaches on vista by doing everything in the all users start menu
  SetShellVarContext all
  SetOutPath $INSTDIR
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\PARPG"
  CreateShortCut "$SMPROGRAMS\PARPG\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\PARPG\Uninstall.lnk" "$INSTDIR\uninstall.exe"
  SetOutPath "$INSTDIR\game" ;this makes the following shortcut run in the installed directory
  CreateShortCut "$SMPROGRAMS\PARPG\PARPG.lnk" "$INSTDIR\game\run.py"
  CreateShortCut "$SMPROGRAMS\PARPG\Editor.lnk" "$INSTDIR\game\parpg_editor.py"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\gui\icons\window_icon.ico"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  ;avoid shortcuts headaches on vista by doing everything in the all users start menu
  SetShellVarContext all
  
  ;Remove all the code
  RMDir /r "$INSTDIR\game\dialogue"
  RMDir /r "$INSTDIR\game\editor"
  RMDir /r "$INSTDIR\game\fonts"
  RMDir /r "$INSTDIR\game\gui"
  RMDir /r "$INSTDIR\game\lib"
  RMDir /r "$INSTDIR\game\local_loaders"
  RMDir /r "$INSTDIR\game\maps"
  RMDir /r "$INSTDIR\game\music"
  RMDir /r "$INSTDIR\game\objects"
  RMDir /r "$INSTDIR\game\quests"
  RMDir "$INSTDIR\game\saves" ;Test if the directory will get deleted when it contains files. The expected behaviour is that it will not.
  RMDir /r "$INSTDIR\game\scripts"
  RMDir /r "$INSTDIR\game\tests"
  RMDir /r "$INSTDIR\game\utilities"
  
  Delete "$INSTDIR\game\dialogue_demo.py"
  Delete "$INSTDIR\game\dialogue_schema.yaml"
  Delete "$INSTDIR\game\PARPG"
  Delete "$INSTDIR\game\parpg_editor.py"
  Delete "$INSTDIR\game\run.py"
  Delete "$INSTDIR\game\run_tests.py"
  Delete "$INSTDIR\game\settings.py"
  Delete "$INSTDIR\game\settings.xml"
  Delete "$INSTDIR\game\README.txt"
  Delete "$INSTDIR\game\log_parpg.bat"
  Delete "$INSTDIR\game\*.log"
  Delete "$INSTDIR\game\*.pyc"
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninstall.exe"
  RMDir "$INSTDIR\game"
  RMDir /r "$INSTDIR\tools"
  
  RMDir "$INSTDIR"

  ;Remove shortcuts
  RMDir /r "$SMPROGRAMS\PARPG"
 
  ;Remove Registry keys
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd
SectionGroup Externals
;---------- DOWNLOAD PYTHON -------
Section "ActivePython (required)" Python
  SetDetailsPrint textonly

  DetailPrint "Downloading Python"
  NSISdl::download http://downloads.activestate.com/ActivePython/releases/2.6.4.10/ActivePython-2.6.4.10-win32-x86.msi $TEMP/pysetup.msi
  Pop $R0 ;Get the return value
    StrCmp $R0 "success" +3
      MessageBox MB_OK "Failed to download Python installer: $R0"
      Quit

  DetailPrint "Installing Python"
  ExecWait '"msiexec" /i "$TEMP\pysetup.msi"'

  DetailPrint "Deleting Python installer"
  Delete $TEMP\pysetup.msi
SectionEnd
;------------FIFE-------------------
Section "FIFE (required)" FIFE
  SetDetailsPrint textonly

  SetOutPath "$TEMP"
  ;Get all the core PARPG files
  FILE /r "dependencies\fife_0.3.0_r3236_win32.exe"
  DetailPrint "Installing FIFE"
  ExecWait "$TEMP\fife_0.3.0_r3236_win32.exe"

  DetailPrint "Deleting FIFE installer"
  Delete "$TEMP\fife_0.3.0_r3236_win32.exe"
SectionEnd
;------------ PyYAML --------------
Section "PyYAML (required)" PyYAML
  SetDetailsPrint textonly

  SetOutPath "$SYSDIR"        ;Some Systems need this DLL to install PyYAML properly
  ;SetOverwrite ifnewer
  ;File "requs\msvcr71.dll"
  ;SetOverwrite on
  NSISdl::download http://pyyaml.org/download/pyyaml/PyYAML-3.09.win32-py2.6.exe $TEMP\pyaml_setup.exe
  Pop $R0 ;Get the return value
    StrCmp $R0 "success" +3
      MessageBox MB_OK "Failed to download PyYAML installer: $R0"
      Quit

  
  SetOutPath "$TEMP"
  DetailPrint "Installing PyYAML"
  ExecWait "$TEMP\pyaml_setup.exe"

  DetailPrint "Deleting PyYAML installer"
  Delete "$TEMP\PyYAML_setup.exe"
SectionEnd
;----------- OPEN AL --------------
Section "OpenAL (required)" OpenAL
  SetDetailsPrint textonly

  ;oalinst.exe must be downloaded seperately and put into the
  ;dependencies directory for packaging to be successful
  SetOutPath "$TEMP"
  File ".\dependencies\oalinst.exe"
  DetailPrint "Installing OpenAL"
  ExecWait "$TEMP\oalinst.exe"

  DetailPrint "Deleting OpenAL installer"
  Delete "$TEMP\oalinst.exe"
SectionEnd
;--------- SECTION END ------------
SectionGroupEnd
LangString DESC_PARPG ${LANG_ENGLISH} "PARPG - Techdemo 1 SVN r522"
LangString DESC_Python ${LANG_ENGLISH} "ActivePython 2.6.4.8 - Required to run PARPG. Requires an active internet connection to install."
LangString DESC_FIFE ${LANG_ENGLISH} "FIFE 0.3.0 SVN trunk r3236 - Required to run PARPG."
LangString DESC_PyYAML ${LANG_ENGLISH} "PyYAML 3.09 - Required Python Module. Requires an active internet connection to install."
LangString DESC_OpenAL ${LANG_ENGLISH} "OpenAL - Required for sound effects and music playback."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${PARPG} $(DESC_PARPG)
  !insertmacro MUI_DESCRIPTION_TEXT ${Python} $(DESC_Python)
  !insertmacro MUI_DESCRIPTION_TEXT ${FIFE} $(DESC_FIFE)
  !insertmacro MUI_DESCRIPTION_TEXT ${PyYAML} $(DESC_PyYAML)
  !insertmacro MUI_DESCRIPTION_TEXT ${OpenAL} $(DESC_OpenAL)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
