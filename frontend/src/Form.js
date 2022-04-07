import { useRef } from "react";

const Form = ({ handleSubmit }) => {
  const replaysRef = useRef([]);

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

  async function readFileAsDataURL(file) {
    let result = await new Promise((resolve) => {
      let fileReader = new FileReader();
      fileReader.onload = () => resolve(fileReader.result);
      fileReader.readAsBinaryString(file);
    });

    // console.log(result); // aGV5IHRoZXJl...

    return result;
  }

  async function decodeAndSubmit(files) {
    const roa_files = files.filter(
      (f) => f.name.substring(f.name.length - 3) === "roa"
    );

    const new_roa_files = roa_files.map((file) => readFileAsDataURL(file));
    await Promise.all(new_roa_files).then((values) => {
      handleSubmit(values);
    });
  }

  return (
    <div>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          decodeAndSubmit(replaysRef.current);
        }}
      >
        {/* <label
          htmlFor="filePicker"
          style={{ background: "grey", padding: "5px 10px" }}
        >
          Upload Replay folder
        </label> */}
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
      </form>
    </div>
  );
};

export default Form;
