export interface Aspirante {
    numero_orden_sorteo: number; // El número de orden en el tribunal, no el del sorteo general
    nombre_apellidos: string;
    numero_orden_alfabetico: number; // El número del sorteo general (opcional, para mostrarlo)
  }