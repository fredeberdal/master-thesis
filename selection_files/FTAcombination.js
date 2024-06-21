import { runFta } from "fta-cli";
import { writeFile } from 'fs/promises';

async function analyzeAndSave() {
    try {
        console.log("------------------ Starting the analysis ----------------");
        let output = await runFta("C:/Users/frede/OneDrive/Dokumenter/1Skole/Master/master_thesis/testprojects/control", { json: true });
        //console.log("FTA Output:", output);
        const outputPath = 'halstead.json';
        if (typeof output === 'string') {
            output = JSON.parse(output);
          }

        if (!output) {
            console.log("No output received from runFta.");
            return; 
        }

        await writeFile(outputPath, JSON.stringify(output, null, 2));
        console.log("Output saved to", outputPath);
        } catch (error) {
        console.error('Error during analyses:', error);
    }
}

analyzeAndSave();

