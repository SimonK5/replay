import { useRef, useState } from "react";

const Form = ({ handleSubmit }) => {
  const replaysRef = useRef([]);
  const [emptyUploadError, setEmptyUploadError] = useState(false);

  function myCustomFileGetter(event) {
    const files = [];
    // Retrieves the files loaded by the drag event or the select event
    const fileList = event.dataTransfer
      ? event.dataTransfer.files
      : event.target.files;

    for (var i = 0; i < fileList.length; i++) {
      const file = fileList.item(i);
      files.push(file);
    }

    // files returned from this function will be acceptedFiles
    return files;
  }

  async function readFileAsText(file) {
    let result = await new Promise((resolve) => {
      let fileReader = new FileReader();
      fileReader.onload = () => resolve(fileReader.result);
      fileReader.readAsBinaryString(file);
    });

    return result;
  }

  async function decodeAndSubmit(roa_files) {
    const roa_files_text = roa_files.map((file) => readFileAsText(file));
    await Promise.all(roa_files_text).then((values) => {
      handleSubmit(values);
    });
  }

  return (
    <div>
      <form
        onSubmit={(e) => {
          e.preventDefault();

          const roa_files = replaysRef.current.filter(
            (f) => f.name.substring(f.name.length - 3) === "roa"
          );

          if (roa_files.length === 0) {
            setEmptyUploadError(true);
          } else {
            setEmptyUploadError(false);
            decodeAndSubmit(roa_files);
          }
        }}
      >
        <input
          id="filePicker"
          type="file"
          name="file[]"
          webkitdirectory=""
          directory=""
          onChange={(e) => {
            const r = myCustomFileGetter(e);
            replaysRef.current = r;
            console.log(replaysRef.current);
          }}
        />

        <button className="btn">Submit</button>
        {emptyUploadError && <p>No valid files uploaded!</p>}
      </form>
    </div>
  );
};

export default Form;
