const fs = require("fs");

const news = [
  {
    titolo: "Aggiornamento calendario scolastico",
    descrizione: "Il Ministero ha aggiornato le date delle vacanze pasquali.",
    data: new Date().toISOString().split("T")[0]
  },
  {
    titolo: "Corso di formazione online",
    descrizione: "Disponibile nuovo corso per la gestione della classe digitale.",
    data: new Date().toISOString().split("T")[0]
  }
];

fs.writeFileSync("newsDocenti.json", JSON.stringify(news, null, 2));
console.log("✅ File JSON creato.");
