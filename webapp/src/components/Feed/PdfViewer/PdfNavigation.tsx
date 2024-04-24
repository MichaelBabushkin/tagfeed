interface NavigationProps {
    pageNumber: number;
    numPages: number;
  }
  
  const PdfNavigation = ({ pageNumber, numPages }: NavigationProps) => (
    <nav className="bg-black">
      <div className="mx-auto px-2 sm:px-6 lg:px-8">
        <div className="relative flex h-16 items-center justify-between">
          <p className="text-2xl font-bold tracking-tighter text-white mx-auto">
            Papermark - Page {pageNumber} / {numPages}
          </p>
        </div>
      </div>
    </nav>
  );

export default PdfNavigation;