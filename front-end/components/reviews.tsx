"use client";
import React from "react";

interface Review {
  id: string;
  description: string;
  sentiment: string;
  created_at: string;
}

interface ReviewsProps {
  data: Review[];
}

export default function Reviews({ data }: ReviewsProps) {
  const [description, setDescription] = React.useState("");
  const [loading, setLoading] = React.useState(false);

  function filterData(id: string) {
    setLoading(true);
    const filteredData = data.filter((review) => review.id === id);
    if (filteredData.length > 0) {
      setDescription(filteredData[0].description);
    } else {
      setDescription("No description available.");
    }
    setLoading(false);
  }

  return (
    <div className="w-full p-4">
      <div className="mb-4 text-lg font-semibold text-center">
        {loading ? "Loading..." : description}
      </div>
      <table className="table-auto w-full border-collapse">
        <thead>
          <tr className="bg-primary text-white">
            <th className="px-2 lg:py-1 w-10">#</th>
            <th className="px-2 text-start">Review</th>
            <th className="px-2 text-start">Category</th>
            <th className="px-2 text-start">Date</th>
            <th className="px-2 text-start">View</th>
          </tr>
        </thead>
        <tbody>
          {data.map((review, index) => (
            <tr key={index} className="border text-sm">
              <td className="text-center w-10">{index + 1}</td>
              <td>{review.description.slice(0, 50)}...</td>
              <td>
                {review.sentiment === "positive" ? (
                  <span className="text-green-500">Positive</span>
                ) : review.sentiment === "negative" ? (
                  <span className="text-red-500">Negative</span>
                ) : (
                  <span className="text-gray-500">Neutral</span>
                )}
              </td>
              <td>{new Date(review.created_at).toDateString()}</td>
              <td>
                <button
                  className="text-blue-500 underline"
                  onClick={() => filterData(review.id)}
                  aria-label={`View review ${index + 1}`}
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
