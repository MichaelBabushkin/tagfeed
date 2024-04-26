import AddTagContainer from "../Tag/AddTagContainer";
import FeedContainer from "../Feed/FeedContainer";
import Modal from "../Modal";
import { ModalProvider } from "../../context/ModalContext";
import { useState } from "react";

function Home() {
  const [filteredTags, setFilteredTags] = useState<string[]>([]);

  return (
    <div>
      <ModalProvider>
        <AddTagContainer
          setFilteredTags={(tags: string[]) => setFilteredTags(tags)}
        />
        <FeedContainer filteredTags={filteredTags} />
        <Modal />
      </ModalProvider>
    </div>
  );
}

export default Home;
