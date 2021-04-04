import '../App.css'
import { useState } from 'react';
import styles from './MainForm.module.css';



function MainForm() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [isLoading, setIsLoading ] = useState(false);
    const [result, setResult] = useState(null);
    const [imageAdded, setImageAdded] = useState(false);

    const handlechange = (e) => {
        setSelectedFile(e.target.files[0])
        setImageAdded(true)
        setResult(null)
    }

	
    const handleSubmission = () => {
        if(!imageAdded) return
        setIsLoading(true)
        let image = new FormData()
        image.append('files', selectedFile)
        console.log(selectedFile)
		fetch(
			'http://localhost:8000/upload/',
			{
				method: 'POST',
                headers: {
                    "accept": "application/json",
                },
				body: image,

			}
		)
			.then((response) => response.json())
			.then((result) => {
				console.log('Success:', result);
                setResult(result)
                setIsLoading(false)
			})
			.catch((error) => {
				console.error('Error:', error);
                setIsLoading(false)

			});
	};
    return (

          <div className={styles.container}>
              <h2 className={styles.title}>Bestand Uploaden</h2>
              <div className={styles.formCard}>
                  <form>
                  <input required type="file" name="files" id="fileinput" accept=".png, .jpg, .jpeg" onChange={handlechange} className={styles.filesinput}/>
                  <label className={styles.buttonBlue} for="fileinput">Bestand Selecteren</label>
                  {imageAdded ? <p>Geselecteerd bestand: {selectedFile.name}</p> : <></>}
                  {isLoading ? <div className={styles.button}><div className={styles.ldsring}><div></div><div></div><div></div><div></div></div></div> : <div id="submit" onClick={handleSubmission} className={styles.button}>Upload</div>}

                  </form>
              </div>
              {result ?
              <>
              <div className={styles.resultCard}>
                  <ul className={styles.resultList}>
                    <li>FileName: {result.UploadedFileName}</li>
                    <li>Age Prediction: {result.age}</li>
                  </ul>
                  </div>
                   </>
                  : <></>}
                  {isLoading ?
                   <div className={styles.resultCard}>
                  <div className={styles.ldsring}><div></div><div></div><div></div><div></div></div>
                  </div> : <></>}
              {(imageAdded || result) ? <img src={URL.createObjectURL(selectedFile)}  alt="result" className={styles.image}/> : <></>}

             
          </div>
    );
  }

 





export default MainForm;
