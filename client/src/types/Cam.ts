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
    name: string;
    ip_address: string;
    user_id: string;
    fire_detected: boolean;
    created_at: string;
    confidence: number;
    last_alert: string | null;
    last_checked: string;
    latitude: number;
    longitude: number;
    last_connected: string;
    status: string;
    email: string;
  }
  export default CamData