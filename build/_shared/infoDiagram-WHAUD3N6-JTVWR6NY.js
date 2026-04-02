import {
  package_default
} from "/ClimateLaboratoryBook/build/_shared/chunk-EYXQDAO3.js";
import {
  selectSvgElement
} from "/ClimateLaboratoryBook/build/_shared/chunk-YZZVRB5P.js";
import {
  parse
} from "/ClimateLaboratoryBook/build/_shared/chunk-OA3SYV6I.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-FLZJMRFV.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-MD55FDMD.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-UH5LSYEI.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-GJ35H52W.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-WGO24YBI.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-UORA2QU4.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-2WSSL7DL.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-5TL5RV2T.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-75Y45RJ5.js";
import {
  configureSvgSize
} from "/ClimateLaboratoryBook/build/_shared/chunk-463FZTZ7.js";
import {
  __name,
  log
} from "/ClimateLaboratoryBook/build/_shared/chunk-7PDOACA3.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-5XJWQ5WJ.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-SP2MKLPW.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-T7QTAV5N.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-2WW6JOYG.js";
import "/ClimateLaboratoryBook/build/_shared/chunk-CGOEG7L2.js";

// ../../node_modules/mermaid/dist/chunks/mermaid.core/infoDiagram-WHAUD3N6.mjs
var parser = {
  parse: /* @__PURE__ */ __name(async (input) => {
    const ast = await parse("info", input);
    log.debug(ast);
  }, "parse")
};
var DEFAULT_INFO_DB = {
  version: package_default.version + (true ? "" : "-tiny")
};
var getVersion = /* @__PURE__ */ __name(() => DEFAULT_INFO_DB.version, "getVersion");
var db = {
  getVersion
};
var draw = /* @__PURE__ */ __name((text, id, version) => {
  log.debug("rendering info diagram\n" + text);
  const svg = selectSvgElement(id);
  configureSvgSize(svg, 100, 400, true);
  const group = svg.append("g");
  group.append("text").attr("x", 100).attr("y", 40).attr("class", "version").attr("font-size", 32).style("text-anchor", "middle").text(`v${version}`);
}, "draw");
var renderer = { draw };
var diagram = {
  parser,
  db,
  renderer
};
export {
  diagram
};
//# sourceMappingURL=/ClimateLaboratoryBook/build/_shared/infoDiagram-WHAUD3N6-JTVWR6NY.js.map
