import Tag from "./Tag";

type TagContainerProps = {
  tags: Array<string>;
  callback?: Function | undefined;
  additionalStyles?: string;
};

function TagContainer({ tags, callback, additionalStyles }: TagContainerProps) {
  return (
    <div className= {`${additionalStyles} my-3 flex flex-wrap -m-1 gap-2`}>
      {tags &&
        tags.map((tag) => (
          <Tag
            key={tag}
            text={tag}
            removeTag={callback ? () => callback(tag) : undefined}
          />
        ))}
    </div>
  );
}

export default TagContainer;
