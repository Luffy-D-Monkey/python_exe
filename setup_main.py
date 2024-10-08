import os
import shutil

# 项目根目录下不用（能）转译的py文件（夹）名，用于启动的入口脚本文件一定要加进来
ignore_files = [
    "build",
    "package",
    ".conda",
    ".vscode",
    "__pycache__",
    ".git",
    "setup.py",
    "setup_main.py",
    "server.py",
    "__init__.py",
    "build_exe.py",
    ".gitignore",
]
# 项目子目录下不用（能）转译的'py文件（夹）名
ignore_names = ["__init__.py"]
# 不需要原样复制到编译文件夹的文件或者文件夹
ignore_move = ["venv", "__pycache__", "server.log", "setup.py", "setup_main.py"]
# 需要编译的文件夹绝对路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 将以上不需要转译的文件(夹)加上绝对路径
ignore_files = [os.path.join(BASE_DIR, x) for x in ignore_files]
# 是否将编译打包到指定文件夹内 (True)，还是和源文件在同一目录下(False)，默认True
package = True
# 打包文件夹名 (package = True 时有效)
package_name = "build_pyd"
# 打包文件夹路径 (package = True 时有效)
package_path = os.path.join(BASE_DIR, package_name)

translate_pys = []


# 编译需要的py文件
def translate_dir(path):
    pathes = os.listdir(path)
    # if path != BASE_DIR and path != '__init__.py' in pathes:
    #     with open(os.path.join(path, '__init__.py'), 'w', encoding='utf8') as f:
    #         pass
    for p in pathes:
        if p in ignore_names:
            continue
        if p.startswith("__") or p.startswith(".") or p.startswith("build"):
            continue
        f_path = os.path.join(path, p)
        if f_path in ignore_files:
            continue
        if os.path.isdir(f_path):
            translate_dir(f_path)
        else:
            if not f_path.endswith(".py") and not f_path.endswith(".pyx"):
                continue
            if f_path.endswith("__init__.py") or f_path.endswith("__init__.pyx"):
                continue
            with open(f_path, "r", encoding="utf8") as f:
                content = f.read()
                if not content.startswith("# cython: language_level=3"):
                    content = "# cython: language_level=3\n" + content
                    with open(f_path, "w", encoding="utf8") as f1:
                        f1.write(content)
            os.system("python setup.py " + f_path + " build_ext --inplace")
            translate_pys.append(f_path)
            f_name = ".".join(f_path.split(".")[:-1])
            py_file = ".".join([f_name, "py"])
            c_file = ".".join([f_name, "c"])
            print(f"f_path: {f_path}, c_file: {c_file}, py_file: {py_file}")
            if os.path.exists(c_file):
                os.remove(c_file)


# 移除编译临时文件
def remove_dir(path, rm_path=True):
    if not os.path.exists(path):
        return
    pathes = os.listdir(path)
    for p in pathes:
        f_path = os.path.join(path, p)
        if os.path.isdir(f_path):
            remove_dir(f_path, False)
            os.rmdir(f_path)
        else:
            os.remove(f_path)
    if rm_path:
        os.rmdir(path)


# 移动编译后的文件至指定目录
def mv_to_packages(path=BASE_DIR):
    pathes = os.listdir(path)
    for p in pathes:
        if p.startswith("."):
            continue
        if p in ignore_move:
            continue
        f_path = os.path.join(path, p)
        if f_path == package_path:
            continue
        p_f_path = f_path.replace(BASE_DIR, package_path)
        if os.path.isdir(f_path):
            if not os.path.exists(p_f_path):
                os.mkdir(p_f_path)
            mv_to_packages(f_path)
        else:
            if not f_path.endswith(".py") or f_path not in translate_pys:
                with open(f_path, "rb") as f:
                    content = f.read()
                    with open(p_f_path, "wb") as f:
                        f.write(content)
            if f_path.endswith(".pyd") or f_path.endswith(".so"):
                os.remove(f_path)


# 将编译后的文件重命名成：源文件名+.pyd，否则编译后的文件名会类似：myUtils.cp39-win_amd64.pyd
def batch_rename(src_path):
    filenames = os.listdir(src_path)
    same_name = []
    count = 0
    for filename in filenames:
        old_name = os.path.join(src_path, filename)
        if old_name == package_path:
            continue
        if os.path.isdir(old_name):
            batch_rename(old_name)
        if filename[-4:] == ".pyd" or filename[-3:] == ".so":
            old_pyd = filename.split(".")
            new_pyd = str(old_pyd[0]) + "." + str(old_pyd[len(old_pyd) - 1])
        else:
            continue
        change_name = new_pyd
        count += 1
        new_name = os.path.join(src_path, change_name)
        if change_name in filenames:
            same_name.append(change_name)
            continue
        os.rename(old_name, new_name)


def build_pyd():
    translate_dir(BASE_DIR)
    remove_dir(os.path.join(BASE_DIR, "build"))

    # 若没有打包文件夹，则生成一个
    if not os.path.exists(package_path):
        os.mkdir(package_path)
    else:
        # 删除重新建
        shutil.rmtree(package_path)
        os.mkdir(package_path)
    if package:
        mv_to_packages()
    batch_rename(os.path.join(BASE_DIR, package_name))


def run():
    build_pyd()


if __name__ == "__main__":
    run()
