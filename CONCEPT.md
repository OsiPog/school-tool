- converts images in the form

  `![...](path/to/an/image.png)`

  or

  `<img src="path/to/image.png" />`

  to

  ```html
[Open Image]({relative_md_file_dir}/{filename}.xopp)
![SCHOOLTOOL]({relative_md_file_dir}/preview/{filename}.png)
```


```rust
Dir
│   md_file.md 
│
└───md_file (folder)
    │   xournal_file.xopp // Is being edited by the user
    │
    └───preview
            preview_image.png // is displayed in the md file that the xopp is actually visible in the MD-file
```



```mermaid
graph TD
new("New Image-Tag has been found!")
-->conv("Convert it to XOPP <br/>move to <i>'FolderForMD/...'</i> subfolder")
-->cre("Create preview image <br/> in <i>'FolderForMD/preview/...'</i> subfolder")
-->fin("Replace image-tag with above syntax")
```
