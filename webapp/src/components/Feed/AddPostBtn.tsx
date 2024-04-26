import { useContext } from "react";
import { ModalContext } from "../../context/ModalContext";

function AddPostBtn() {
  const { setOpen } = useContext(ModalContext);

  const openModal = () => {
    if (setOpen) {
      setOpen(true);
    }
  };

  return (
    <div
      className="relative inline-flex items-center justify-center px-7 py-4
      overflow-hidden font-mono font-medium tracking-tighter
      text-white bg-gray-800 rounded-full group hover:cursor-pointer"
      onClick={openModal}
    >
      <span className="absolute w-0 h-0 transition-all duration-500 ease-out bg-green-500 rounded-full group-hover:w-56 group-hover:h-56"></span>
      <span className="absolute inset-0 w-full h-full -mt-1 rounded-lg opacity-30 bg-gradient-to-b from-transparent via-transparent to-gray-700"></span>
      <span className="relative text-3xl font=semibold">+</span>
    </div>
  );
}

export default AddPostBtn;
