import { Dropzone, FileMosaic } from "@dropzone-ui/react";

import { useState } from "react";

function DragAndDrop() {
  const [files, setFiles] = useState<any>([]);
  const [, setImageSrc] = useState(undefined);
  const updateFiles = (incommingFiles: Array<object>) => {
    console.log("incomming files", incommingFiles);
    setFiles(incommingFiles);
  };
  const onDelete = (id: any) => {
    setFiles(files.filter((x:any) => x.id !== id));
  };
  const handleSee = (imageSource: any) => {
    setImageSrc(imageSource);
  };

  return (
    <Dropzone
      onChange={updateFiles}
      value={files}
      maxFiles={10}
      maxFileSize={2998000}
    >
      {files.map((file: any) => (
        <FileMosaic
          {...file}
          onDelete={onDelete}
          onSee={handleSee}
          preview
          info
          hd
        />
      ))}
    </Dropzone>
  );
}

export default DragAndDrop;
