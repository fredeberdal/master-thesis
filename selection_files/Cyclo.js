import { writeFile } from 'fs/promises';
import { runFta } from "fta-cli"; 

async function analyzeAndSave() {
    try {
        let output = await runFta("C:/Users/frede/OneDrive/Dokumenter/1Skole/Master/master_thesis/prosjektA", { json: true });
        //console.log("FTA Output:", output);

        if (!output) {
            console.log("No output received from runFta.");
            return;
        }

        if (typeof output === 'string') {
            output = JSON.parse(output);
        }

        // Sort the array descending order
        output.sort((a, b) => b.cyclo - a.cyclo);

        const outputPath = 'halstead.json';
        await writeFile(outputPath, JSON.stringify(output, null, 2));
        console.log("Output saved to", outputPath);
    } catch (error) {
        console.error('Error during processing:', error);
    }
}

analyzeAndSave();
