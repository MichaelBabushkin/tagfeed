import { useEffect, useState } from "react";
// import { useCallback, useEffect, useMemo, useRef, useState } from "react";
// import { useInfiniteQuery } from "react-query";
import TagContainer from "../Tag/TagContainer";
import sampleData from "../../sampleData.json";
import VisualContent from "./VisualContent";
import TextContainer from "./TextContainer";
import AddPostBtn from "./AddPostBtn";

// const MAX_POST_PAGE = 1;

// interface TodoType {
//   id: number;
//   title: string;
// }

// const fetchTodos = async ({ pageParam }: { pageParam: number }) => {
//   const response = await fetch(
//     `https://jsonplaceholder.typicode.com/todos?_pages=${pageParam}&_limit=${MAX_POST_PAGE}`
//   );
//   const todos = (await response.json()) as TodoType[];
//   return todos;
// };

interface FeedContainerProps {
  filteredTags: string[];
}

const FeedContainer = ({ filteredTags }: FeedContainerProps) => {
  // const observer = useRef<IntersectionObserver>();

  // const { data, error, fetchNextPage, hasNextPage, isFetching, isLoading } =
  //   useInfiniteQuery({
  //     queryKey: ["feed_posts"],
  //     queryFn: ({ pageParam }) => fetchTodos({ pageParam }),
  //     getNextPageParam: (lastPage, allPages) => {
  //       return lastPage.length ? allPages.length + 1 : undefined;
  //     },
  //   });

  // const lastElementRef = useCallback(
  //   (node: HTMLDivElement) => {
  //     if (isLoading) return;

  //     if (observer.current) observer.current.disconnect();

  //     observer.current = new IntersectionObserver((entries) => {
  //       if (entries[0].isIntersecting && hasNextPage && !isFetching) {
  //         // fetchNextPage();
  //       }
  //     });

  //     if (node) observer.current.observe(node);
  //   },
  //   [fetchNextPage, hasNextPage, isFetching, isLoading]
  // );

  // const todos = useMemo(() => {
  //   return data?.pages.reduce((acc, page) => {
  //     return [...acc, ...page];
  //   }, []);
  // }, [data]);

  // if (isLoading) return <h1>Carregando mais dados...</h1>;

  // if (error) return <h1>Erro ao carregar os dados</h1>;

  const [posts, SetPosts] = useState(sampleData);

  useEffect(() => {
    if (filteredTags.length === 0) {
      SetPosts(sampleData);
    } else {
      const filteredPosts = sampleData.filter((post) =>
        post.tags.some((tag) => filteredTags.includes(tag))
      );
      SetPosts(filteredPosts);
    }
  }, [filteredTags]);

  return (
    <>
      {posts &&
        posts.map((item) => (
          <div
            className="container my-24 mx-auto md:px-6"
            key={item.id}
            // ref={lastElementRef}
          >
            <section className="mb-32 text-center">
              <div className="mb-12 flex flex-wrap justify-center">
                <VisualContent item={item} />

                <div className="w-full shrink-0 grow-0 basis-auto px-3 md:w-8/12 xl:w-6/12">
                  <TagContainer
                    tags={item.tags}
                    additionalStyles="justify-center"
                  />

                  <p className="mb-4 text-neutral-500 dark:text-neutral-300">
                    <small>
                      Published on: <u>{item.date}</u>
                    </small>
                  </p>
                  <TextContainer description={item.description} />
                </div>
              </div>
            </section>
            {/* {isFetching && <div>Loading more posts...</div>} */}
          </div>
        ))}
      <div className="fixed bottom-2 right-2">
        <AddPostBtn />
      </div>
    </>
  );
};

export default FeedContainer;
