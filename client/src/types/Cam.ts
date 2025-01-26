interface RelatedPark {
    states: string;
    parkCode: string;
    designation: string;
    fullName: string;
    url: string;
    name: string;
  }
  
  interface CamData {
    _id: string;
    id: string;
    url: string;
    title: string;
    description: string;
    images: string[];
    relatedParks: RelatedPark[];
    status: string;
    statusMessage: string;
    isStreaming: boolean;
    tags: string[];
    latitude: number;
    longitude: number;
    geometryPoiId: string;
    credit: string;
    confidence: number
  }
  export default CamData