import { useContext, useEffect, useState } from "react";
import { ModalContext } from "../context/ModalContext";
import DragAndDrop from "./FileUpload/DragAndDrop";

export default function Modal() {
  const [showModal, setShowModal] = useState<boolean>(false);
  const [tags, setTags] = useState<Array<string>>([]);
  const [inputTag, setInputTag] = useState("");
  const { open, setOpen } = useContext(ModalContext);

  useEffect(() => {
    setShowModal(() => open);
  }, [open]);

  const closeModal = () => {
    if (setOpen) {
      setOpen(false);
    }
  };

  const saveChanges = () => {
    console.log("Save Changes");
    if (setOpen) {
      setOpen(false);
    }
  };

  const handleAddTag = (): void => {
    if (inputTag && !tags.includes(inputTag)) {
      setTags([...tags, inputTag]);
      setInputTag("");
    }
  };

  const handleDeleteTag = (tagToDelete: string): void => {
    setTags(tags.filter((tag) => tag !== tagToDelete));
  };

  if (!showModal) return null;

  return (
    <>
      <div className="fixed inset-0 z-50 flex items-center justify-center overflow-hidden bg-black bg-opacity-25">
        <div className="relative mx-auto my-6 max-w-4xl w-full px-4">
          <div className="bg-white rounded-lg shadow-2xl relative flex flex-col">
            <div className="flex items-start justify-between p-5 border-b border-gray-200 rounded-t">
              <h3 className="text-2xl font-semibold">Add New Content</h3>
              <button
                onClick={closeModal}
                className="text-3xl text-gray-600 hover:text-gray-800 cursor-pointer"
                aria-label="Close"
              >
                &times;
              </button>
            </div>
            <div className="p-6 flex-auto">
              <DragAndDrop />
              <div className="mt-4 flex items-center gap-2">
                <input
                  type="text"
                  placeholder="Add a tag"
                  value={inputTag}
                  onChange={(e) => setInputTag(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleAddTag();
                      e.preventDefault(); // Prevent form submission
                    }
                  }}
                  className="input-field flex-1 p-3 text-lg border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={handleAddTag}
                  className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-r-md rounded-l-md p-6 text-xl text-center transition duration-200 ease-in-out shadow"
                >
                  +
                </button>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {tags.map((tag, index) => (
                  <span
                    key={index}
                    className="bg-blue-100 text-blue-800 text-lg font-semibold mr-2 px-4 py-2 rounded-full flex items-center"
                  >
                    {tag}
                    <button
                      onClick={() => handleDeleteTag(tag)}
                      className="ml-2 text-red-500 text-xl"
                    >
                      &times;
                    </button>
                  </span>
                ))}
              </div>
              <textarea
                placeholder="Description"
                className="mt-4 p-3 border border-gray-300 rounded-md w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div className="flex items-center justify-center p-6 border-t border-gray-200">
              <button
                onClick={closeModal}
                className="bg-red-500 hover:bg-red-600 text-white rounded-full py-2 px-6 transition duration-200 ease-in-out shadow"
              >
                Close
              </button>
              <button
                onClick={saveChanges}
                className="ml-3 bg-green-500 hover:bg-green-600 text-white rounded-full py-2 px-6 transition duration-200 ease-in-out shadow"
              >
                Save Changes 💾
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
