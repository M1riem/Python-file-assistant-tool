:: �⪫�砥� �⮡ࠦ���� ⥪�饩 �������
@echo off
:: �������� ��������� ����: replacement of numbers
title replacement of numbers
::������ 梥� ���� .bat: ᢥ⫮-����� �㪢� �� �஬ 䮭�
Color 8E   
:: ������ � �����稪� �㦭� �� ����� ࠧ �뢮���� ���ଠ樮���� ����?
echo �� �ணࠬ�� ������� �᫠ n �� ��������� ���祭�� �� �᫠ (n+delta) � ��࠭�� ���� 䠩�� '.fos' ��� '.MSG'. ���� '.MSG' �㤥� ������� � ������ � ���᪮� � ������᪮� ����������� �����६���� 
::������⢮ ����७�� ��� ��ᨢ��� ��ॢ��� ��ப�
set /a n=5
::��砫� ��᪮��筮�� 横��
for /l %%i in (0 0 0) do (
python C:\GitHub\Python\Python-file-assistant-tool\menu.py
::--------------------------------------------------------------
call :print %n%
)
pause
exit /B

:print
for /l %%i in (1 1 %1) do <nul set /p strTemp=--------------------
echo.
for /l %%i in (1 1 %1) do <nul set /p strTemp=--------------------
echo.
echo.
echo.
exit /B