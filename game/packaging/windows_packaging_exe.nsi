!define PRODUCT_NAME "PARPG"
!define PRODUCT_VERSION "SVN trunk r522"
!define PRODUCT_PUBLISHER "PARPG Development Team"
!define PRODUCT_WEB_SITE "http://www.parpg.net/"
!define INSTDIR_REG_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define INSTDIR_REG_ROOT "HKLM"
!define PARPG_DIR ".."

; MUI 1.67 compatible ------
!include "MUI.nsh"

;include the Uninstall log header
!include "AdvUninstLog2.nsh"

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
InstallDirRegKey ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "InstallDir"
ShowInstDetails show
ShowUnInstDetails show

!insertmacro UNATTENDED_UNINSTALL

;------------ Main. Packages PARPG code --------------
Section "PARPG" PARPG
  SectionIn RO
  SetOverwrite try
  
  ;Get all the core PARPG files
  SetOutPath "$INSTDIR\game\dialogue\"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE /r /x ".svn" "${PARPG_DIR}\dialogue\"
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  SetOutPath "$INSTDIR\game\fonts\"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE /r /x ".svn" "${PARPG_DIR}\fonts\"
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  SetOutPath "$INSTDIR\game\gui\"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE /r /x ".svn" "${PARPG_DIR}\gui\"
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  SetOutPath "$INSTDIR\game\maps\"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE /r /x ".svn" "${PARPG_DIR}\maps\"
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  SetOutPath "$INSTDIR\game\music\"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE /r /x ".svn" "${PARPG_DIR}\music\"
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  SetOutPath "$INSTDIR\game\objects\"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE /r /x ".svn" "${PARPG_DIR}\objects\"
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  SetOutPath "$INSTDIR\game\quests\"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE /r /x ".svn" "${PARPG_DIR}\quests\"
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  SetOutPath "$INSTDIR\game"
  !insertmacro UNINSTALL.LOG_OPEN_INSTALL
  FILE "${PARPG_DIR}\dist\*"
  FILE "${PARPG_DIR}\settings-dist.xml"
  
  FILE "${PARPG_DIR}\README"

  RENAME "settings-dist.xml" "settings.xml"
  RENAME "README" "README.txt"
  
  CreateDirectory "$INSTDIR\game\saves"  
  CreateDirectory "$INSTDIR\game\screenshots"  
  !insertmacro UNINSTALL.LOG_CLOSE_INSTALL
  
  SetAutoClose true
SectionEnd
/*
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
*/
Section -AdditionalIcons
  ;avoid shortcuts headaches on vista by doing everything in the all users start menu
  SetShellVarContext all
  SetOutPath $INSTDIR
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateDirectory "$SMPROGRAMS\${PRODUCT_NAME}"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk" "${UNINST_EXE}"
  SetOutPath "$INSTDIR\game" ;this makes the following shortcut run in the installed directory
  CreateShortCut "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk" "$INSTDIR\game\Parpg.exe"
  ;CreateShortCut "$SMPROGRAMS\PARPG\Editor.lnk" "$INSTDIR\game\parpg_editor.py"
SectionEnd

Section -Post
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "UninstallString" "$INSTDIR\uninstall.exe"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "DisplayIcon" "$INSTDIR\gui\icons\window_icon.ico"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Function .onInit

        ;prepare log always within .onInit function
        !insertmacro UNINSTALL.LOG_PREPARE_INSTALL

FunctionEnd


Function .onInstSuccess

         ;create/update log always within .onInstSuccess function
         !insertmacro UNINSTALL.LOG_UPDATE_INSTALL

FunctionEnd

Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "$(^Name) was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove $(^Name) and all of its components?" IDYES +2
  Abort
FunctionEnd

Section UnInstall
    ;Remove files
    Delete "$INSTDIR\${PRODUCT_NAME}.url"
    !insertmacro UNINSTALL.NEW_UNINSTALL "$OUTDIR"
    ;Remove shortcuts    
    Delete "$SMPROGRAMS\${PRODUCT_NAME}\Website.lnk"
    Delete "$SMPROGRAMS\${PRODUCT_NAME}\Uninstall.lnk"
    Delete "$SMPROGRAMS\${PRODUCT_NAME}\${PRODUCT_NAME}.lnk"
    RmDir "$SMPROGRAMS\${PRODUCT_NAME}"
    ;Remove Registry keys
    DeleteRegKey ${INSTDIR_REG_ROOT} "${INSTDIR_REG_KEY}"
    SetAutoClose true

SectionEnd

LangString DESC_PARPG ${LANG_ENGLISH} "PARPG - Techdemo 1 SVN r522"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${PARPG} $(DESC_PARPG)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
