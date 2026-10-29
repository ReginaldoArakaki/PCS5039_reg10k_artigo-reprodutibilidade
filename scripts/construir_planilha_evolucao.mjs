import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const artifactEntry = require.resolve("@oai/artifact-tool", { paths: ["C:/Users/Reginaldo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"] });
const { SpreadsheetFile, Workbook } = await import(pathToFileURL(artifactEntry).href);

const repo = process.argv[2];
const outputDir = process.argv[3];
const data = JSON.parse(await fs.readFile(path.join(repo, "dados", "evolucao", "workbook-data.json"), "utf8"));
const workbook = Workbook.create();
const navy = "#17365D", blue = "#2F75B5", pale = "#D9EAF7", green = "#70AD47", amber = "#ED7D31", gray = "#F2F2F2";
const font = "Aptos";

function title(sheet, text, subtitle, cols = 8) {
  sheet.showGridLines = false;
  sheet.mergeCells(`A1:${String.fromCharCode(64 + Math.min(cols, 26))}1`);
  sheet.getRange("A1").values = [[text]];
  sheet.getRange("A1").format = { fill: navy, font: { name: font, size: 18, bold: true, color: "#FFFFFF" }, rowHeight: 30 };
  sheet.mergeCells(`A2:${String.fromCharCode(64 + Math.min(cols, 26))}2`);
  sheet.getRange("A2").values = [[subtitle]];
  sheet.getRange("A2").format = { fill: pale, font: { name: font, size: 10, color: navy }, wrapText: true, rowHeight: 30 };
}

function addTableSheet(name, subtitle, headers, rows, widths) {
  const s = workbook.worksheets.add(name);
  title(s, name, subtitle, headers.length);
  s.getRangeByIndexes(3, 0, rows.length + 1, headers.length).values = [headers, ...rows];
  const h = s.getRangeByIndexes(3, 0, 1, headers.length);
  h.format = { fill: blue, font: { name: font, bold: true, color: "#FFFFFF" }, wrapText: true, verticalAlignment: "center" };
  const body = s.getRangeByIndexes(4, 0, Math.max(rows.length, 1), headers.length);
  body.format.font = { name: font, size: 10 };
  body.format.borders = { preset: "all", style: "thin", color: "#D9E2F3" };
  body.format.wrapText = true;
  widths.forEach((w, i) => s.getRangeByIndexes(0, i, rows.length + 4, 1).format.columnWidth = w);
  s.freezePanes.freezeRows(4);
  if (rows.length) s.tables.add(`A4:${String.fromCharCode(64 + headers.length)}${rows.length + 4}`, true, `${name.replace(/[^A-Za-z0-9]/g, "")}Table`);
  return s;
}

const resumo = workbook.worksheets.add("Resumo");
title(resumo, "Evolução experimental Reg10k", "PCS5039 · evidências observadas em 29/10/2026; v1dt.1 mantida separadamente como proposta", 12);
resumo.getRange("A4:D4").values = [["Indicador", "V0", "V1", "V2"]];
resumo.getRange("A5:D9").values = [
  ["Cômodos", ...data.versoes.map(r => r[5])],
  ["Cenários", ...data.versoes.map(r => r[7])],
  ["Execuções", ...data.versoes.map(r => r[8])],
  ["LOC rastreadas", ...data.versoes.map(r => data.estaticas.find(x => x[0] === r[0] && x[1] === "loc_total")?.[2] ?? null)],
  ["Eventos médios/cômodo (referência)", ...data.versoes.map(r => data.dinamicas.find(x => x[0] === r[0] && x[1] === "referencia" && x[3] === "n_eventos")?.[10] ?? null)],
];
resumo.getRange("A4:D4").format = { fill: blue, font: { name: font, bold: true, color: "#FFFFFF" } };
resumo.getRange("A5:D9").format = { font: { name: font, size: 11 }, borders: { preset: "all", style: "thin", color: "#D9E2F3" } };
resumo.getRange("B5:D8").format.numberFormat = "0";
resumo.getRange("B9:D9").format.numberFormat = "0.00";
resumo.getRange("A11:F11").values = [["Leitura", "Interpretação", "Implicação para o artigo", "Status", "Prioridade", "Próxima evidência"]];
resumo.getRange("A12:F16").values = [
  ["Escala espacial", "1→2→4 cômodos no mesmo núcleo", "Usar normalização por cômodo e tempo ocupado", "observado", "alta", "comparação pareada"],
  ["Massa experimental", "5.580 execuções em 30 sementes", "Relatar dispersão e IC, não só médias", "observado", "alta", "bootstrap por cenário"],
  ["Cobertura", "F1–F7 cobrem operação, FP/FN, falha, rede e DT", "Estratificar resultados por família", "observado", "alta", "tabela família × versão"],
  ["Comportamento", "F8–F10 adicionam múltiplos ocupantes, sono e suspeita", "Nova hipótese sobre inteligência no Hub", "planejado", "alta", "rodada v1dt.1"],
  ["Digital Twin", "Fidelidade resulta de percepção + sincronização", "Separar causas locais e de conectividade", "observado", "alta", "decomposição do erro"],
];
resumo.getRange("A11:F11").format = { fill: navy, font: { name: font, bold: true, color: "#FFFFFF" }, wrapText: true };
resumo.getRange("A12:F16").format = { font: { name: font, size: 10 }, borders: { preset: "all", style: "thin", color: "#D9E2F3" }, wrapText: true, verticalAlignment: "center" };
resumo.getRange("D12:D14").format.fill = "#E2F0D9";
resumo.getRange("D15").format.fill = "#FFF2CC";
resumo.getRange("D16").format.fill = "#E2F0D9";
resumo.getRange("A:A").format.columnWidth = 27;
resumo.getRange("B:F").format.columnWidth = 23;
resumo.freezePanes.freezeRows(4);
resumo.getRange("H20:I23").values = [["Versão", "Cenários"], ...data.versoes.map(r => [r[0], r[7]])];
resumo.getRange("H20:I23").format.font = { name: font, color: "#FFFFFF" };
const c1 = resumo.charts.add("bar", resumo.getRange("H20:I23"));
c1.title = "Cenários por versão";
c1.titleTextStyle.typeface = font;
c1.legend = { position: "top", textStyle: { typeface: font } };
c1.setPosition("H4", "N17");

const versoes = addTableSheet("Versões", "Commits e dimensões observados nas tags publicadas", ["Versão","Tag","Commit tag","Commit main","Núcleo","Cômodos","Moradores modelados","Cenários","Execuções","Estado"], data.versoes, [11,12,44,44,15,10,18,11,12,13]);
versoes.getRange(`F5:I${data.versoes.length + 4}`).format.numberFormat = "0";

const estaticas = addTableSheet("Métricas estáticas", "Contagem na árvore Git de cada tag; arquivos derivados e submódulo não são expandidos", ["Versão","Métrica","Valor","Unidade","Tag"], data.estaticas, [11,25,14,14,12]);
estaticas.getRange(`C5:C${data.estaticas.length + 4}`).format.numberFormat = "0";

const dinamicas = addTableSheet("Métricas dinâmicas", "Sínteses de 5.580 execuções; família TODAS; preserve estratificação por controlador", ["Versão","Controlador","Família","Métrica","N","Média","Mediana","Desvio padrão","Mínimo","Máximo","Média por cômodo"], data.dinamicas, [10,20,11,30,10,15,15,17,14,14,20]);
dinamicas.getRange(`E5:E${data.dinamicas.length + 4}`).format.numberFormat = "0";
dinamicas.getRange(`F5:K${data.dinamicas.length + 4}`).format.numberFormat = "0.00";

const propostas = addTableSheet("Experimentos", "Agenda recomendada; itens propostos não devem ser confundidos com dados já coletados", ["ID","Nome","Escopo","Métricas / método","Finalidade","Prioridade"], data.experimentos, [9,25,18,42,40,12]);
propostas.getRange(`F5:F${data.experimentos.length + 4}`).conditionalFormats.add("containsText", { text: "alta", format: { fill: "#FCE4D6", font: { color: "#9C0006", bold: true } } });

const plano = workbook.worksheets.add("v1dt.1 planejada");
title(plano, "v1dt.1 — marco planejado", "A especificação é fonte de hipóteses e desenho experimental; não contém resultados medidos", 8);
plano.getRange("A4:B12").values = [
  ["Campo", "Definição"], ["Base", "nucleo-v1.3; planta V1"], ["Variável alterada", "ocupantes"],
  ["População", "morador, moradora, criança, idoso, Rex e visitante"], ["F8", "ocupação múltipla: um sai e outro fica"],
  ["F9", "dormir: compromisso entre escuro acordado e luz com todos dormindo"], ["F10", "presença incompatível e conciliação de passagem tardia"],
  ["Métrica nova", "luz_com_todos_dormindo_s"], ["Métricas F10", "precisão, revocação, latência de confirmação, conciliações e eventos de fronteira"],
];
plano.getRange("A4:B4").format = { fill: amber, font: { name: font, bold: true, color: "#FFFFFF" } };
plano.getRange("A5:B12").format = { font: { name: font, size: 11 }, borders: { preset: "all", style: "thin", color: "#D9E2F3" }, wrapText: true };
plano.getRange("A:A").format.columnWidth = 23;
plano.getRange("B:B").format.columnWidth = 75;
plano.freezePanes.freezeRows(4);

const fontes = addTableSheet("Fontes", "Proveniência, hashes SHA-256 e condição de uso", ["Fonte","Caminho","SHA-256","Uso"], data.fontes, [20,75,68,28]);

workbook.recalculate();
await fs.mkdir(outputDir, { recursive: true });
for (const name of ["Resumo", "Versões", "Métricas estáticas", "Métricas dinâmicas", "Experimentos", "v1dt.1 planejada", "Fontes"]) {
  const preview = await workbook.render({ sheetName: name, autoCrop: "all", scale: 0.8, format: "png" });
  await fs.writeFile(path.join(outputDir, `preview-${name.replace(/[^A-Za-z0-9]/g, "-")}.png`), new Uint8Array(await preview.arrayBuffer()));
}
const scan = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, maxChars: 4000 });
console.log(scan.ndjson ?? scan);
const overview = await workbook.inspect({ kind: "sheet,table,drawing", maxChars: 6000, tableMaxRows: 4, tableMaxCols: 8 });
console.log(overview.ndjson ?? overview);
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(path.join(outputDir, "base-evolucao-reg10k-pcs5039-20261029.xlsx"));
