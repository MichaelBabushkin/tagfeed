import { createContext, ReactNode, useState } from "react";

type Props = {
  children?: ReactNode;
};

type IModalContext = {
  open: boolean;
  setOpen?: (newState: boolean) => void;
};

const initialValue: IModalContext = {
  open: false,
};

const ModalContext = createContext<IModalContext>(initialValue);

const ModalProvider = ({ children }: Props) => {
  const [open, setOpen] = useState(initialValue.open);

  return (
    <ModalContext.Provider value={{ open, setOpen }}>
      {children}
    </ModalContext.Provider>
  );
};

export { ModalContext, ModalProvider };
