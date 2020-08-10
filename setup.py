from cx_Freeze import setup, Executable

setup(
    name='Test',
    version='1.0',
    description='Test EXE',
    executables=[Executable('main.py')], requires=['docx']
)