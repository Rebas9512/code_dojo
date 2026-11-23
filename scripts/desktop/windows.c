#include <windows.h>
#include <wchar.h>
#include <stdlib.h>

/* 只定位安装目录并启动完整解释器。路径和参数支持空格、中文。 */
int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR args, int show) {
    wchar_t base[32768], python[32768], command[32768];
    DWORD length = GetModuleFileNameW(NULL, base, 32768);
    if (!length || length >= 32768) return 1;
    wchar_t *slash = wcsrchr(base, L'\\');
    if (!slash) return 1;
    *slash = L'\0';
    if (swprintf_s(python, 32768, L"%ls\\python\\pythonw.exe", base) < 0 ||
        swprintf_s(command, 32768, L"\"%ls\" -I -B \"%ls\\start.py\"", python, base) < 0) return 1;
    STARTUPINFOW startup = {sizeof(startup)};
    PROCESS_INFORMATION process = {0};
    if (!CreateProcessW(python, command, NULL, NULL, FALSE, 0, NULL, base, &startup, &process)) {
        MessageBoxW(NULL, L"无法打开内置 Python，请先完整解压安装包。", L"code-dojo", MB_ICONERROR);
        return 1;
    }
    CloseHandle(process.hThread);
    CloseHandle(process.hProcess);
    return 0;
}
