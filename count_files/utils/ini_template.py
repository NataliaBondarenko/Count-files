import configparser

from count_files.settings import DST_INI


# for --help-cmd, help> config about
help_readme = \
    '\nCount Files Configuration File.\nContains the data needed to sort file extensions by type. ' \
    'If the file does not exist, it is created on demand using --sort-type argument with value - "default".\n' \
    'Sample sections in the file count_files.ini:\n[python]\nextensions = py, pyw, pyc\n' \
    '[misc]\nextensions = png, html, md\n...\n' \
    'Sections names.\n' \
    'Sections names are case-sensitive. ' \
    'If possible, keep the section name in one word. ' \
    'If the section name consists of several words, then the snake_case is highly recommended.\n' \
    'Section names containing spaces, argparse prefix chars (`-` or `--`) at the beginning of a name, ' \
    'or characters with special meanings are not recommended. ' \
    'Because user input is performed from the terminal. ' \
    'In addition, the section names in this file must be unique, like the keys in the Python dictionary.\n' \
    'Customization.\n' \
    'All extension groups can be created, renamed, updated, and deleted. ' \
    'You can create your own extension groups in the appropriate format. ' \
    'Please note that the section name is also used as a title when displaying extension count results.\n' \
    'Keys and values IN sections.\n' \
    'Keys in sections are case-insensitive. Key values in sections are stored as a string. ' \
    'In this case, it is a string with file extensions separated by comma and space. ' \
    '`extensions` is a required key inside a section. ' \
    'Values can also span multiple lines, as long as they are indented deeper than the first line of the value. ' \
    'Compound extensions are not processed here. ' \
    'To search and count compound extensions, use the `--filename-match` argument.\n' \
    'Extensions that do not fit any of the selected types are displayed below with other files. ' \
    'If you use `--case-sensitive` argument and among the extensions found there are the same extensions, ' \
    'but in a different register, they will be displayed below with other files. ' \
    'If the same extension is specified in different groups, ' \
    'then when sorting it will be assigned to the group ' \
    'that is listed first in the type list after the --sort-type argument.\n' \
    'If you explicitly specify the path to the folder, ' \
    'then it should not be after the argument --sort-type so that it does not fall into the list of types.\n' \
    'Extended interpolation.\n' \
    'You can use extended interpolation ' \
    '(https://docs.python.org/3/library/configparser.html#configparser.ExtendedInterpolation). ' \
    'This allows values to contain format strings that reference values in other sections.\n' \
    'Example:\n[section_name]\nextensions = ${section_1:extensions}, ${section_2:extensions}'

readme = r"""# Count Files Configuration File.
# Contains the data needed to sort file extensions by type.
# If the file does not exist, it is created on demand using `--sort-type` argument with value - "default".
# Predefined extension groups. This extension groups can be renamed, updated, and deleted.
#   [archives] - Archives and compressed files.
#   [audio_video], [audio], [videos], [images] - Media files.
#   [data] - Data and configuration files, databases, spreadsheets (numbers, ods, xls, xlsx).
#   [documents] - Various text, markup, office files (text and presentations).
#   [executables] - Executable code, executable file, or executable program, Shell scripts, installation archives.
#   [fonts] - Fonts.
#   [microsoft_office], [libre_office] - Microsoft Office and LibreOffice (OpenDocument) extensions.
#   Programming languages: Python, JavaScript, Java, PHP, C/C++, C#
# Data from this file is processed by the ConfigParser module:
#   https://docs.python.org/3/library/configparser.html
# ConfigParser sections names.
#   ConfigParser sections names are case-sensitive. If possible, keep the section name in one word.
#   If the section name consists of several words, then the snake_case is highly recommended.
#   Section names containing spaces, argparse prefix chars (`-` or `--`) at the beginning of a name,
#   or characters with special meanings are not recommended.
#   Because user input is performed from the terminal.
#   In addition, the section names in this file must be unique, like the keys in the Python dictionary.
# Customization.
#   All extension groups can be created, renamed, updated, and deleted.
#   You can create your own extension groups in the appropriate format.
#   Please note that the section name is also used as a title when displaying extension count results.
# Example in count_files.ini file:
#   [section_name]
#    extensions = py, pyw, pyc
# Result in the terminal:
#   + SECTION NAME(57)
#       PYC: 30
#       PY: 27
#   + + + (15)
#       other files here
#       ...
# Keys and values IN sections.
#   Keys in sections are case-insensitive. Key values in sections are stored as a string.
#   In this case, it is a string with file extensions separated by comma and space.
#   `extensions` is a required key inside a section.
#   Values can also span multiple lines, as long as they are indented deeper than the first line of the value.
#   Compound extensions are not processed here.
#   To search and count compound extensions, use the `--filename-match` argument.
# Extensions that do not fit any of the selected types are displayed below with other files.
# If the same extension is specified in different groups, then when sorting it will be assigned to the group 
# that is listed first in the type list after the `--sort-type` argument. 
# If you explicitly specify the path to the folder, then it should not be after the argument --sort-type 
# so that it does not fall into the list of types.
# If you use `--case-sensitive` argument and among the extensions found there are the same extensions, 
# but in a different register, they will be displayed below with other files.
# Example:
#   + SECTION NAME(30)
#       txt: 30
#   + + + (45)
#       md: 12
#       TXT: 5
#       ...
# Extended interpolation.
#   You can use extended interpolation
#   (https://docs.python.org/3/library/configparser.html#configparser.ExtendedInterpolation).
#   This allows values to contain format strings that reference values in other sections.
# Example:
#   [section_name]
#    extensions = ${section_1:extensions}, ${section_2:extensions}
#
"""

d = {
    'DEFAULT': {},
    'archives': {'extensions': '7z, arc, arj, bz, bz2, bzip2, cab, dar, gz, gzip, jar, lz, lzma, '
                               'rar, shar, shr, tar, tbz, tbz2, tg, tgz, txz, xz, zip, zipx'},
    'audio_video': {'type': 'media containers are used to encapsulate audio and/or video',
                    'extensions': '3gp, 3gp2, 3gpp, 3gpp2, mp4, mpeg, mpg, ogg, webm'},
    'audio': {'extensions': 'aac, aif, aiff, amr, cda, flac, mp1, mp2, mp3, m4a,  mid, midi, '
                            'mka, mpa, oga, wav, wave, wma'},
    'videos': {'extensions': 'asf, avchd, avi, flv, h264, m4v, mkv, mov, mpv, ogm, ogv, ogx, '
                             'rm, rmvb, qt, qtff, swf, vob, wmv'},
    'images': {'extensions': 'apng, bmp, dib, djv, djvu, gif, ico, icon, jfif, jpeg, jpg, '
                             'pic, pict, pjp, pjpeg, pjpg, png, raw, svg, svgz, tif, tiff'},
    'data': {'extensions': 'accdb, accdc, accde, cfg, conf, csv, dat, data, database, db, dbf, '
                           'geojson, ini, json, log, mdb, mysql, numbers, odb, ods, pdb, sqlite, sqlite3, '
                           'sqlitedb, topojson, torrent, tsv, wndb, xls, xlsx, xml, yaml, yml'},
    'documents': {'extensions': 'abw, bib, bibtex, doc, docx, epub, latex, ltx, markdn, markdown, '
                                'md, mdown, odp, ott, pdf, ppt, pptx, pub, rst, rtf, tex, text, txt'},
    'executables': {'extensions': 'a, action, apk, app, applescript, application, appref-ms, ba_, bash, '
                                  'bat, bin, bsh, cmd, com, command, csh, deb, dll, elf, ex_, exe, ipa, ksh, lib, '
                                  'mpkg, msi, o, ps1, ps2, psc1, psc2, run, sh, so, tcsh, vbe, vbs, workflow, wsf, zsh'},
    'fonts': {'extensions': 'fon, font, ttf, woff, woff2'},
    'microsoft_office': {'extensions': 'accda, accdb, accdc, accde, accdp, accdr, accdt, accdu, acl, ade, asd, '
                                       'cnv, crtx, doc, docm, docx, dot, dotm, dotx, grv, h1q, iaf, laccdb, maf, mam, '
                                       'maq, mar, mat, maw, mda, mdb, mde, mdt, mdw, mpd, mpp, mpt, mso, oab, obi, '
                                       'oft, olm, one, onepkg, ops, ost, pa, pip, pot, potm, potx, ppa, ppam, pps, '
                                       'ppsm, ppsx, ppt, pptm, pptx, prf, pst, pub, puz, rpmsg, sldm, sldx, slk, snp, '
                                       'svd, thmx, vdx, vsd, vsdx, vss, vst, vsx, vtx, wbk, wll, xar, xl, xla, xlam, '
                                       'xlb, xlc, xll, xlm, xls, xlsb, xlsm, xlsx, xlt, xltm, xltx, xlw, xsf, xslb, xsn'},
    'libre_office': {'extensions': 'bau, doc, dump, fodg, fodp, fods, fodt, odb, odc, odf, odg, odi, odm, odp, '
                                   'ods, odt, oos, oot, otc, otf, otg, oth, oti, otp, ots, ott, oxt, psw, pub, sda, '
                                   'sdb, sdc, sdd, sdp, sds, sdv, sdw, sfs, sgl, smd, smf, sms, sob, soe, stc, std, '
                                   'sti, stw, svm, sxc, sxd, sxg, sxi, sxm, sxw, uot, vor, xlb'},
    'html_files': {'extensions': 'chm, cshtml, dhtml, htc, htm, html, html5, htx, jhtml, mhtm, mhtml, phtm, '
                                 'phtml, rhtml, shtm, shtml, vbhtml, xhtm, xhtml'},
    'style_files': {'extensions': 'css, less, pcss, postcss, qss, sass, scss'},
    'python_files': {'extensions': 'egg, egg-info, egg-link, epp, ipy, ipynb, npy, npz, oog, p4a, pck, pcl, '
                                   'pickle, pil, pth, pxd, pxi, py, py2, py3, py3tb, pyc, pyd, pyde, pyi, pym, pyo, '
                                   'pyp, pyproj , pyt, pytb, pyw, pyx, pyz, pyzw, rpy, whl'},
    'javascript_files': {'extensions': 'js, mjs, coffee, ejs, ts, tsx, es, es6, jsx, jss, jgz, _js, bones, cjs, '
                                       'frag, gs, jake, jsb, jscad, jsfl, jsm, njs, pac, sjs, ssjs, xsjs, xsjslib'},
    'java_files': {'extensions': 'class, ear, j, jad, jar, jav, java, jnlp, jsp, mf, properties'},
    'php_files': {'extensions': 'phl, php, php2, php3, php4, php5, phpproj, phps, phpt'},
    'c_files': {'extensions': 'c, cats, h, idc'},
    'cpp_files': {'extensions': 'c++, cc, chh, cp, cpp, cxx, h, h++, hh, hpp, hxx, inc, inl, ino, ipp, re, tcc, tpp'},
    'csharp_files': {'extensions': 'c#, cake, cs, csx'}

}


def generate_ini_file():
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read_dict(d)
    with open(DST_INI, 'w') as f:
        for i in readme.split('\n'):
            f.write(f"{i}\n")
    with open(DST_INI, 'a') as configfile:
        config.write(configfile)
