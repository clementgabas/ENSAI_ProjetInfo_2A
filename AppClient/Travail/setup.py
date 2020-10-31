from cx_Freeze import setup, Executable

setup(
	name = "ApplicationClient",
	version = "1",
	description = "Premier éxécutable pour l'application client",
	executables = [Executable("appClient.py")]
)