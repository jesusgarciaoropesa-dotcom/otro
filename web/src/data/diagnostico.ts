// Grupos de síntomas para la página "¿Qué le pasa a mi planta?".
// Cada grupo apunta a artículos por su id (slug). El orden importa: se muestra
// tal cual. Un artículo puede repetirse en dos grupos si encaja en ambos.

export interface GrupoDiagnostico {
  id: string;
  emoji: string;
  titulo: string;
  descripcion: string;
  articulos: string[];
}

export const gruposDiagnostico: GrupoDiagnostico[] = [
  {
    id: 'hojas-amarillas',
    emoji: '💛',
    titulo: 'Las hojas se ponen amarillas',
    descripcion: 'Amarilleo general o por zonas. Casi siempre es riego, nutrientes o falta de hierro.',
    articulos: [
      'por-que-tomateras-se-ponen-amarillas',
      'hojas-amarillas-pimiento-causas-solucion',
      'hojas-amarillas-limonero-citricos-maceta',
      'por-que-se-caen-hojas-plantas-huerto-urbano',
    ],
  },
  {
    id: 'manchas-hojas',
    emoji: '🍂',
    titulo: 'Manchas o polvo en las hojas',
    descripcion: 'Manchas blancas, marrones o polvillo: suele ser un hongo o el ambiente.',
    articulos: [
      'oidio-huerto-urbano-como-eliminarlo',
      'mildiu-tomatera-como-tratarlo',
      'manchas-blancas-hojas-plantas-que-son',
      'bordes-hojas-marrones-secos-causas',
      'hojas-aguacate-marrones-secas-que-hacer',
    ],
  },
  {
    id: 'hojas-rizadas',
    emoji: '🌀',
    titulo: 'Hojas rizadas o deformadas',
    descripcion: 'Se enrollan, se rizan o salen deformes. A veces es calor; a veces, plaga.',
    articulos: [
      'hojas-rizadas-tomatera-causas',
      'minador-citricos-hojas-rizadas-limonero',
    ],
  },
  {
    id: 'bichos',
    emoji: '🐛',
    titulo: 'Veo bichos en la planta',
    descripcion: 'Insectos visibles en tallos, hojas o el envés. Identifícalos y trátalos a tiempo.',
    articulos: [
      'como-eliminar-pulgon-plantas-balcon-natural',
      'como-eliminar-mosca-blanca-huerto-balcon',
      'como-eliminar-arana-roja-plantas-balcon',
      'cochinilla-algodonosa-como-eliminarla-balcon',
      'trips-huerto-balcon-como-eliminarlos',
      'chinches-huerto-tomate-como-eliminarlas',
      'como-eliminar-caracoles-babosas-balcon',
      'como-eliminar-hormigas-macetas-balcon',
      'oruga-col-kale-brocoli-como-eliminarla',
      'tuta-absoluta-tomate-como-eliminarla',
      'gusano-del-fruto-tomate-pimiento-heliothis',
      'gusano-gris-lechugas-como-eliminarlo',
      'como-eliminar-saltamontes-esperanza-plantas-balcon',
    ],
  },
  {
    id: 'tierra',
    emoji: '🪴',
    titulo: 'Problemas en la tierra o las raíces',
    descripcion: 'Mosquitos del sustrato, moho, larvas o tierra que no absorbe el agua.',
    articulos: [
      'mosca-sustrato-mosquitos-macetas-eliminar',
      'moho-blanco-tierra-macetas',
      'gusano-blanco-maceta-como-eliminarlo',
      'como-evitar-exceso-riego-hongo-macetas',
      'tierra-maceta-no-absorbe-agua-compactada',
      'gomosis-hongos-raiz-citricos-limonero-seco',
    ],
  },
  {
    id: 'frutos',
    emoji: '🍅',
    titulo: 'Los frutos salen mal',
    descripcion: 'Manchas, grietas, deformaciones o podredumbre en tomates, pimientos o calabacines.',
    articulos: [
      'culo-negro-tomate-podredumbre-apical',
      'culo-negro-pimiento',
      'por-que-se-rajan-los-tomates',
      'manchas-amarillas-tomates-maduracion-irregular',
      'cara-de-gato-tomate-deformado-cicatrices',
      'calabacin-pepino-se-pudre-punta',
      'se-caen-frutos-pequenos-sin-madurar',
    ],
  },
  {
    id: 'flores',
    emoji: '🌸',
    titulo: 'Se caen las flores o no cuaja',
    descripcion: 'Mucha planta y pocos frutos, o flores que caen sin cuajar.',
    articulos: [
      'flores-tomate-caen-sin-cuajar',
      'flores-pimiento-se-caen-sin-cuajar',
      'brocoli-coliflor-no-forma-cabeza',
      'pocos-tomates-muchas-hojas-mas-cosecha',
      'pimiento-mucha-mata-pocos-frutos',
    ],
  },
  {
    id: 'se-seca',
    emoji: '🥀',
    titulo: 'La planta se seca o se marchita',
    descripcion: 'Decae, pierde la hoja o se viene abajo. Casi siempre es un tema de raíz y agua.',
    articulos: [
      'como-revivir-planta-marchita-maceta',
      'como-evitar-exceso-riego-hongo-macetas',
      'gomosis-hongos-raiz-citricos-limonero-seco',
    ],
  },
];

// Artículos de tratamientos y prevención, para el bloque final.
export const tratamientosDiagnostico: string[] = [
  'como-prevenir-plagas-huerto-urbano-sin-pesticidas',
  'jabon-potasico-plagas-como-usarlo',
  'aceite-neem-huerto-como-usarlo',
  'tierra-diatomeas-huerto',
  'trampas-cromaticas-amarillas-plagas',
  'plantas-repelentes-plagas-huerto',
  'atraer-insectos-beneficiosos-huerto',
  'remedios-caseros-plagas-que-no-funcionan',
];
