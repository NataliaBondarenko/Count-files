[English](https://github.com/victordomingos/Count-files/blob/master/README.md) | [Portugu&ecirc;s](https://github.com/victordomingos/Count-files/blob/master/docs/README_PT.md) | [&#x420;&#x443;&#x441;&#x441;&#x43A;&#x438;&#x439;](https://github.com/victordomingos/Count-files/blob/master/docs/README_RU.md) | **[&#x423;&#x43A;&#x440;&#x430;&#x457;&#x43D;&#x441;&#x44C;&#x43A;&#x430;](https://github.com/victordomingos/Count-files/blob/master/docs/README_UA.md)**
  
  
# Count Files [![Github commits (since latest release)](https://img.shields.io/github/commits-since/victordomingos/Count-files/latest.svg)](https://github.com/victordomingos/Count-files)

������ ���������� ����� (CLI), �������� �� Python. � ��������� ���� �������� ����� ������������ �� ������ ����� � ������ �����������, ��� ���������� �� �� �����, ��������� �� �� ����������, � ������ ��������.

![Count Files_screenshot - counting files by extension](https://user-images.githubusercontent.com/18650184/42160179-29998a52-7dee-11e8-9813-b8594e50fe77.png)


## ������������

- [���������](https://countfiles.readthedocs.io/en/latest/)

## ������������

### �� �������� ��������� �������

Count Files - �� �������������� ��������, ��� ���� ���� ����������� � ��������� [pip](https://pip.pypa.io/en/stable/quickstart/):

```
pip3 install count-files
```

������� ����� �������� ������� ����� ���������� � [`pip3 install -e`](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs).

### �� iPhone �� iPad (� Pythonista 3 ��� iOS)

����� ���� ����������������� �� iOS (iPhone/iPad) � ��������� ���������� ����� [StaSh](https://github.com/ywangd/stash) � ������� Pythonista 3.  
����� ��������� ���� � [������������](https://countfiles.readthedocs.io/en/latest/installation.html) �� ������������. 

## ���������

��� ������� ������� ����� Python 3.6+.

## �� ���������������

��� �������� ������ ��������� ��������� �� �������� ���� �� ������������ ������ ������ ���� � ��������� ������:

```
count-files -h
```

```
count-files --help
```

�� ������������� �������� ������� ��������� �� ����� ����� ���������� � ��������� �������� ������� �� � ��� ���� �����������. �������� ����� �� �������� �����������.
���������� �� ������������� �� ������ �� �������. ��������� ��� `ini` �� `INI` ���� ���������.

�� ���� ����� ������� path �� ������� �����, ������ ������������� ��������� �� �����, ������ ����� ���������� ������ ����������, �������� ��������� �� ����� � ���������� ������ �� ������.  
����� �������� ��������� ��������� ���������� ��� ����� ������� ���������� ����� �� �������� ��������� �������� ��� ��������� �����.  
����� ��������: [��������� CLI](https://countfiles.readthedocs.io/en/latest/howtouse.html#cli-arguments).

������� ������� �������� ������������ � ������ ������ ������� ��� ����-���� ���������� ���������. ����������� ����� ���� �������, �� ������ ������� ��� ������� ���������� ����� (���������: .txt, .py, .html, .css) �� �������� ������� ��������� �����.

```
count-files
```

���� ������� ���������� ���� �������� ������ � ������ ����� � ���������� �����������. ��������� ������ ������ - ������ ��� ��������� ������ �� �����.

```
count-files -fe txt [path]
```  
```
count-files --file-extension txt [path]
```

����� ����� ������������ ����� �������� ������� ����� � ������ �����������.

```
count-files -t py [path]
```  
```
count-files --total py [path]
```

��� ��������� ���������� ��� ����� ��� ����������, �������������� ���� ������ �� ����� ��� ����������.

```
count-files -fe . [path]
```  
```
count-files --file-extension . [path]
```

```
count-files -t . [path]
```  
```
count-files --total . [path]
```

���� ��� ������ �� �����, ��������� �� �� ����������, �������������� �� ������ �� ����� ��� ����������.

```
count-files -fe .. [path]
```  
```
count-files --file-extension .. [path]
```

```
count-files -t .. [path]
```  
```
count-files --total .. [path]
```

## �� ������� ������� �� ���� ���������� ���� �������������?

���� �����, �������� ������� � ����� Issues ��� �������� pull request � [���������](https://github.com/victordomingos/Count-files).
