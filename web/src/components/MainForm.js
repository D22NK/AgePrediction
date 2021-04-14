// Importeren van de styles en benodigde functies.
import '../App.css'
import { useState } from 'react';
import styles from './MainForm.module.css';



function MainForm() {
    // Variabelen die worden gebruikt voor het bijhouden van bepaalde resultaten en acties.
    const [selectedFile, setSelectedFile] = useState(null);
    const [isLoading, setIsLoading ] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(false);
    const [imageAdded, setImageAdded] = useState(false);

    // Op het moment dat er een verandering is in het upload formulier zorgt deze functie dat de nieuwe foto op de website wordt laten zien.
    const handlechange = (e) => {
        // De functie wijzigt de variabelen.
        setSelectedFile(e.target.files[0])
        setImageAdded(true)
        setResult(null)
    }

	// Op het moment dat je op de upload knop drukt zorgt deze functie ervoor dat de foto naar de server wordt gestuurd.
    const handleSubmission = () => {
        // Resetten van variabelen.
        setResult(null)
        setError(false)
        // Check of er wel een foto is geselecteerd
        if(!imageAdded) return
        // Zorgen dat de laad spinner wordt laten zien in de upload knop
        setIsLoading(true)
        // Het aanmaken van de data die naar de api gaat worden gestuurd.
        let image = new FormData()
        image.append('files', selectedFile)
        console.log(selectedFile)
        // Het verzoek naar de api maken inclusief de afbeelding.
		fetch(
			'https://ai.d22nk.nl/upload/',
			{
				method: 'POST',
                headers: {
                    "accept": "application/json",
                },
				body: image,

			}
		)
        // Het antwoord van de api gebruiken.
			.then((response) => response.json())
			.then((result) => {
				console.log('Success:', result);
                // Het resultaat van de api zichtbaar maken op de website en de laad spinner weghalen
                setResult(result)
                setIsLoading(false)
			})
            // Als de api een error geeft wordt dat hier verder geregeld.
			.catch((error) => {
				console.error('Error:', error);
                // De error wordt op de website laten zien.
                setIsLoading(false)
                setError(true)
			});
	};

    // Het zichbare deel van de website wordt hier doorgegeven aan App.js
    return (
          <div className={styles.container}>
              <h2 className={styles.title}>Bestand Uploaden</h2>
              <div className={styles.formCard}>
                  {/* Het formulier waar je de afbeelding kan selecteren */}
                  <form>
                  <input required type="file" name="files" id="fileinput" accept=".png, .jpg, .jpeg" onChange={handlechange} className={styles.filesinput}/>
                  <label className={styles.buttonBlue} for="fileinput">Bestand Selecteren</label>
                  {imageAdded ? <p>Geselecteerd bestand: {selectedFile.name}</p> : <></>}
                  {/* Als de variabele isLoading op True staat wordt de laad spinner laten zien, staat hij op False dan zie je de normale knop. */}
                  {isLoading ? <div className={styles.button}><div className={styles.ldsring}><div></div><div></div><div></div><div></div></div></div> : <div id="submit" onClick={handleSubmission} className={styles.button}>Upload</div>}

                  </form>
              </div>
              {/* Als er een resultaat aanwezig is dan wordt de resultcard hier laten zien. */}
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
                  {/* Als de error variabele op True staat wordt er hier een error bericht weergegeven. */}
                  {error ?  <div className={styles.errorCard}><p>Er ging iets fout!</p></div> : <p></p>}
                  {isLoading ?
                   <div className={styles.resultCard}>
                  <div className={styles.ldsring}><div></div><div></div><div></div><div></div></div>
                  </div> : <></>}
            {/* Als de variabele imageAdded True is dan wordt de afbeelding laten zien, anders gebeurt er niks*/}
              {(imageAdded || result) ? <img src={URL.createObjectURL(selectedFile)}  alt="result" className={styles.image}/> : <></>}

             
          </div>
    );
  }

 





export default MainForm;
