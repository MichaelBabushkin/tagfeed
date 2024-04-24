import { useEffect, useRef, useState } from "react";
import TagContainer from "./TagContainer";

interface AddTagContainerProps {
  setFilteredTags: (tags: string[]) => void;
}

function AddTagContainer({ setFilteredTags }: AddTagContainerProps) {
  const [tags, setTags] = useState<string[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);

  const addTag = (event: React.MouseEvent) => {
    event.preventDefault();
    let newTag = checkedInput();
    if (newTag) {
      setTags((prevTags) => [...prevTags, newTag]);
    }
    if (inputRef.current !== null) {
      inputRef.current.value = "";
    }
  };

  const checkedInput = () => {
    if (inputRef.current !== null && !tags.includes(inputRef.current.value)) {
      let checkedInput = inputRef.current.value;
      return checkedInput;
    }
    return "";
  };

  const removeTag = (text: string) => {
    let filteredTagArr = tags.filter((tag) => tag !== text);
    setTags(filteredTagArr);
  };

  useEffect(() => {
    setFilteredTags(tags);
  }, [tags]);

  return (
    <div>
      <div className="mt-12 flex flex-col space-y-4 items-center mx-4 sm:mx-0">
        <div className="py-8 px-8 pt-16 items-center rounded shadow-lg overflow-hidden w-full sm:w-11/12 md:max-w-xl hover:shadow-xl bg-white dark:bg-gray-800">
          <div className="flex flex-row justify-start items-center">
            <h1 className="text-lg sm:text-2xl font-bold text-gray-800 mr-2 dark:text-gray-100">
              Tags
            </h1>
            <div>
              <span className="group relative">
                <div className="absolute bottom-[calc(100%+0.5rem)] left-[50%] -translate-x-[50%] hidden group-hover:block w-auto">
                  <div className="bottom-full right-0 rounded bg-black px-4 py-1 text-xs text-white w-[8rem] h-full text-center">
                    You can filter data with tags to find it faster.
                    <svg
                      className="absolute left-0 top-full h-2 w-full text-black"
                      x="0px"
                      y="0px"
                      viewBox="0 0 255 255"
                      xmlSpace="preserve"
                    >
                      <polygon
                        className="fill-current"
                        points="0,0 127.5,127.5 255,0"
                      />
                    </svg>
                  </div>
                </div>

                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6 text-gray-600 dark:text-gray-300"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </span>
            </div>
          </div>
          <form action="#" className="mt-8">
            <div className="flex bg-gray-100 p-1 items-center w-full space-x-2 sm:space-x- rounded border border-gray-500 dark:bg-gray-700 dark:border-gray-300">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6 opacity-50 dark:text-gray-100 ml-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                />
              </svg>
              <input
                className="bg-gray-100 outline-none text-sm sm:text-base w-full dark:bg-gray-700 dark:text-gray-200 border-transparent focus:border-transparent focus:ring-0"
                type="text"
                ref={inputRef}
                placeholder="Search by tag..."
              />
              <button
                type="submit"
                className="flex-none rounded-md bg-white px-3.5 py-3 text-sm font-semibold text-gray-900 shadow-sm hover:bg-gray-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white hover:scale-105"
                onClick={(e) => addTag(e)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3"
                  />
                </svg>
              </button>
            </div>
          </form>

          <TagContainer tags={tags} callback={removeTag} />
        </div>
      </div>
    </div>
  );
}

export default AddTagContainer;
