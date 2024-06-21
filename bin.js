#!/usr/bin/env node
const { exec } = require('child_process');
const fs = require('fs-extra');
const path = require('path');
const util = require('util');
const execProm = util.promisify(exec);

console.log("-------------------Starting script---------------");

// Flatten directory structure into a new folder
async function flattenDirectory(sourceDir, targetDir) {
    const entries = await fs.readdir(sourceDir, { withFileTypes: true });
    await fs.ensureDir(targetDir);
    for (const entry of entries) {
        const sourcePath = path.join(sourceDir, entry.name);
        if (entry.isDirectory()) {
            await flattenDirectory(sourcePath, targetDir); // Recurse into directories
        } else {
            // Only moving specific file types
            if (entry.name.match(/\.(js|ts|jsx|tsx)$/)) {
                const targetPath = path.join(targetDir, entry.name);
                if (await fs.pathExists(targetPath)) {
                    console.warn(`File exists already. Now overwritten: ${targetPath}`);
                }
                await fs.move(sourcePath, targetPath, { overwrite: true });
                console.log(`Moved file: ${sourcePath} -> ${targetPath}`);
            }
        }
    }
}

// Run cyclomatic complexity on all files in a directory
async function analyzeFiles(directory) {
  const command = `npx cyclomatic-complexity '${directory}/**/*.{js,ts}' --json`;
  console.log("Running command:", command); // Loggin the command for clearity and error detection.

  try {
      const { stdout, stderr } = await execProm(command, { shell: 'C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe' });
      if (stderr) {
          console.error("Error running cyclomatic complexity:", stderr);
      }
      if (stdout) {
          return JSON.parse(stdout);
      }
      return [];
  } catch (error) {
      console.error("Cyclomatic Complexity execution failed :", error);
      return [];
  }
}


// Function to analyze the results
async function analyzeData(results) {
    console.log(' --------------------- Analyzing data ------------------');
    const highestComplexitySumFiles = findHighestComplexitySum(results);
    console.log('Files with the highest complexity:' + highestComplexitySumFiles);

    //const highestComplexityLevelFiles = findFilesWithHighestComplexityLevel(results, 'error');
    //console.log('Files with the highest complexity level (Error):');
    //console.log(highestComplexityLevelFiles);
}

// Sorting and filtering functions
function findHighestComplexitySum(data) {
    return data.sort((a, b) => b.complexitySum - a.complexitySum).slice(0, 5);
}

//function findFilesWithHighestComplexityLevel(data, level) {
//    return data.filter(item => item.complexityLevel === level);
//}

async function main() {
  const srcDir = 'testprojects/prosjektA'; // Original source directory
  const allFilesDir = 'testprojects/prosjektA/allFiles'; // New directory for flattened files
  try {
      await flattenDirectory(srcDir, allFilesDir);
      const results = await analyzeFiles(allFilesDir);
      await fs.writeFile('output.json', JSON.stringify(results, null, 2));
      console.log("Output saved to output.json");
      await analyzeData(results);
  } catch (error) {
      console.error("An error has occurred:", error);
  }
}

main();

