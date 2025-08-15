import { privateApi } from './axios.ts'; // use privateApi for auth requests

export const downloadAuctionPdf = async (tournamentId: string) => {
  try {
    const response = await privateApi.get(
      `/tournament/${tournamentId}/export-auction`,
      { responseType: "blob" }
    );

    // Extract filename from Content-Disposition header
    const contentDisposition = response.headers['content-disposition'];
    let fileName = "Auction_Summary.pdf"; // fallback
    if (contentDisposition) {
      const match = contentDisposition.match(/filename="?([^"]+)"?/);
      if (match?.[1]) fileName = match[1];
    }

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    return true;
  } catch (err) {
    console.error("Error downloading PDF:", err);
    return false;
  }
};
