import PDFViewer from "./PdfViewer/PdfViewer";
import zipImage from "../../assets/zip_file.jpg";

type VisualContentProps = {
  item: {
    id: number;
    tags: string[];
    type: string;
    filename: string;
    content: string;
    description: string;
    date: string;
  };
};

const chooseContentType = (contentType: string, src?: string) => {
  switch (contentType) {
    case "zip":
      return <img src={zipImage} className="w-full" />;
    case "pdf":
      return (
        <div
          className="relative mb-6 overflow-hidden rounded-lg bg-cover bg-no-repeat shadow-lg dark:shadow-black/20"
          data-te-ripple-init
          data-te-ripple-color="light"
        >
          <PDFViewer />
        </div>
      );
    case "image":
      return (
        <div
          className="relative mb-6 overflow-hidden rounded-lg bg-cover bg-no-repeat shadow-lg dark:shadow-black/20"
          data-te-ripple-init
          data-te-ripple-color="light"
        >
          <img src={src} className="w-full" />
        </div>
      );
    case "video":
      return <img src={src} className="w-full" />;
  }
};

function VisualContent({ item }: VisualContentProps) {
  return (
    <div className="w-full shrink-0 grow-0 basis-auto px-3 md:w-10/12">
      {chooseContentType(item.type, item.content)}
      <h5 className="mb-3 text-lg font-bold">{item.filename}</h5>
      {/* <a href="#!">
        <div className="absolute top-0 right-0 bottom-0 left-0 h-full w-full overflow-hidden bg-fixed opacity-0 transition duration-300 ease-in-out hover:opacity-100 bg-[hsla(0,0%,98.4%,.15)]"></div>
      </a> */}
    </div>
  );
}

export default VisualContent;
