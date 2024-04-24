import { useState } from "react";
import ArrowBigDownDashIcon from "../Icons/ArrowBigDownDashIcon";

type TextContainerProps = {
  description: string;
};

function TextContainer({ description }: TextContainerProps) {
  const [readMore, setReadMore] = useState(false);

  return (
    <>
      {readMore ? (
        <p className="mb-6">{description}</p>
      ) : (
        <p className="mb-6 transition">{`${description.substring(
          0,
          250
        )}...`}</p>
      )}
      <button
        className="btn transition ease-in-out duration-700 "
        onClick={() => setReadMore((prev) => !prev)}
      >
        {readMore ? (
          "show less"
        ) : (
          <div className="flex flex-col items-center">
            Read more <div className="animate-bounce"><ArrowBigDownDashIcon /></div>
          </div>
        )}
      </button>
    </>
  );
}

export default TextContainer;
