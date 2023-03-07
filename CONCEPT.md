# Concept

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
    │
    └───xopp
    │   	xournal_file.xopp // Is being edited by the user
    │
    └───preview
            preview_image.png // is displayed in the md file that the xopp is actually visible in the MD-file
```



## `find_and_convert()` (Simplified)

```mermaid
graph TD
new("Image-Tag has been found!")
conv("Convert it to XOPP <br/>move to <i>'FolderForMD/xopp/...'</i> subfolder")
cre("Create preview image <br/> in <i>'FolderForMD/preview/...'</i> subfolder")
fin("Replace image-tag with above syntax")
move("Move XOPP if its on the wrong directory")

q_st{"Is SchoolTool<br> file?"}

new-->q_st
q_st-->|No|conv

q_st-->|Yes|move-->cre

subgraph  
conv-->fin
end


conv-->cre
```
