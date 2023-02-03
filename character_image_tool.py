
from character_psd import CharacterPsd
import sys
import os
import shutil

def main():

    import_file_paths = sys.argv

    # 実行ファイルをリストから消す
    import_file_paths.reverse()
    import_file_paths.pop()

    if  len(sys.argv) < 1 :
        exit()
    
    for import_file_path in import_file_paths :
        # psdファイルなら出力
        if os.path.splitext( import_file_path )[1] == ".psd" :
            psd_to_pngs(import_file_path)

def psd_to_pngs( import_psd_path ):

    # 入力するpsdファイルパス
    import_psd_path = import_psd_path
    # 出力するフォルダパス
    export_path = os.path.dirname(import_psd_path)

    print(import_psd_path)
    print(export_path)
    
    psd = CharacterPsd( import_psd_path )
    dir_path = export_path + "/" + psd.name
    
    # 既に存在する場合は削除
    print("dir path")
    print(psd.name)
    if os.path.exists( dir_path ):
        shutil.rmtree( dir_path )
    os.makedirs( dir_path )
    
    print(psd.name + " export")
    psd.export_group_save(dir_path)

main()