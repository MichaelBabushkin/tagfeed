import { useCallback, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import ChevronLeftIcon from "../../Icons/ChevronLeftIcon";
import ChevronRightIcon from "../../Icons/ChevronRightIcon";
import samplePdf from "./hw.pdf";
import PdfNavigation from "./PdfNavigation";

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.js`;

export default function PDFViewer() {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [loading, setLoading] = useState(true);
  const [pageWidth, setPageWidth] = useState(0);

  const onDocumentLoadSuccess = useCallback(
    ({ numPages }: { numPages: number }) => {
      setNumPages(numPages);
      setLoading(false);
    },
    []
  );

  const onPageLoadSuccess = useCallback(() => {
    setPageWidth(window.innerWidth * 0.8);
  }, []);

  const goToNextPage = useCallback(() => {
    setPageNumber((prevPageNumber) => Math.min(prevPageNumber + 1, numPages));
  }, [numPages]);

  const goToPreviousPage = useCallback(() => {
    setPageNumber((prevPageNumber) => Math.max(prevPageNumber - 1, 1));
  }, []);

  return (
    <>
      <PdfNavigation pageNumber={pageNumber} numPages={numPages} />
      {!loading && (
        <div className="flex items-center justify-between absolute z-10 w-full p-2">
          <button
            onClick={goToPreviousPage}
            disabled={pageNumber <= 1}
            className="relative h-[calc(100vh - 64px)] p-6"
          >
            <ChevronLeftIcon className="h-10 w-10" aria-hidden="true" />
          </button>
          <button
            onClick={goToNextPage}
            disabled={pageNumber >= numPages}
            className="relative h-[calc(100vh - 64px)] p-6"
          >
            <ChevronRightIcon className="h-10 w-10" aria-hidden="true" />
          </button>
        </div>
      )}

      <div className="flex justify-center mx-auto h-full">
        <Document file={samplePdf} onLoadSuccess={onDocumentLoadSuccess}>
          <Page
            pageNumber={pageNumber}
            onLoadSuccess={onPageLoadSuccess}
            width={pageWidth}
            renderAnnotationLayer={false}
            renderTextLayer={false}
          />
        </Document>
      </div>
    </>
  );
}
