import React, { useState, useEffect, useRef } from "react";
import logo from "./logo.svg";
import "./App.css";
import Switch from "@mui/material/Switch";
import ReactMarkdown from "react-markdown";
import Tooltip from "@mui/material/Tooltip";
import SendIcon from "@mui/icons-material/Send";
import RestoreIcon from "@mui/icons-material/Restore";
import InterpreterModeIcon from "@mui/icons-material/InterpreterMode";
import Button from "@mui/material/Button";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import Typography from "@mui/material/Typography";
import ArrowDownwardIcon from "@mui/icons-material/ArrowDownward";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CloseIcon from "@mui/icons-material/Close";

import { styled } from "@mui/material/styles";

function App() {
	const [open, setOpen] = React.useState(false);

	const handleResetChat = () => {
		console.log("reset chat");
		setOpen(true);
	};

	const handleClose = () => {
		setOpen(false);
	};

	const VisuallyHiddenInput = styled("input")({
		clip: "rect(0 0 0 0)",
		clipPath: "inset(50%)",
		height: 1,
		overflow: "hidden",
		position: "absolute",
		bottom: 0,
		left: 0,
		whiteSpace: "nowrap",
		width: 1,
	});
	// const [agencyName, setAgencyName] = useState("");
	// const [agencyDescription, setAgencyDescription] = useState("");
	// const [industry, setIndustry] = useState("");
	// const [location, setLocation] = useState("");
	// const [keywords, setKeywords] = useState("");
	// const [targetAudience, setTargetAudience] = useState("");
	const [agencyName, setAgencyName] = useState("FSRH");
	const [agencyDescription, setAgencyDescription] = useState(
		"Sexual and reproductive Healthcare membership organisation"
	);
	const [industry, setIndustry] = useState("Healthcare");
	const [location, setLocation] = useState("UK");
	const [keywords, setKeywords] = useState(
		"healthcare, womens health, education and training, contraception, menopause, abortion"
	);
	const [targetAudience, setTargetAudience] = useState(
		"Doctors, GPs, nurses, midwifes, pharmacists, nhs"
	);
	// const baseUrl = "http://localhost:8000";
	const baseUrl = "https://fadf-38-242-164-43.ngrok-free.app";
	const [counter, setCounter] = useState(0);
	const [loading, setLoading] = useState(false);
	const loadingMessages = [
		"Collecting videos..",
		"Analyzing data..",
		"Generating insights..",
		"Aggregating data..",
		"Finishing up..",
	];

	const [userInput, setUserInput] = useState("");

	const [videoResults, setVideoResults] = useState(null);
	const [welcomeMessage, setWelcomeMessage] = useState([
		{
			role: "assistant",
			content:
				"Hi " +
				agencyName +
				"! You have selected 3 videos. Would you like to chat about them? 💬 Or I could also run a focus group session to evaluate the selected videos from different perspectives. 🧐",
		},
	]);
	const [chatMessages, setChatMessages] = useState(welcomeMessage);

	const [chatState, setChatState] = useState(false);

	const [videoSelected, setVideoSelected] = useState([]);

	const [messageCounter, setMessageCounter] = useState(0);

	const [timeLeft, setTimeLeft] = useState(140);

	const [uploadResults, setUploadResults] = useState(null);

	// Update the countdown every 1 second
	useEffect(() => {
		let interval;
		if (loading && timeLeft > 0) {
			interval = setInterval(() => {
				setTimeLeft((prevTimeLeft) => prevTimeLeft - 1);
			}, 1000);
		}
		return () => clearInterval(interval);
	}, [loading, timeLeft]);

	// Update the message counter every 20 seconds
	useEffect(() => {
		let messageInterval;
		if (loading) {
			messageInterval = setInterval(() => {
				setMessageCounter(
					(prevMessageCounter) =>
						(prevMessageCounter + 1) % loadingMessages.length
				);
			}, 16000);
		}
		return () => clearInterval(messageInterval);
	}, [loading]);

	const startCountdown = () => {
		setTimeLeft(140);
		setMessageCounter(0);
		setLoading(true);
	};
	const chatWindowRef = useRef(null);

	useEffect(() => {
		if (chatWindowRef.current) {
			chatWindowRef.current.scrollTop =
				chatWindowRef.current.scrollHeight;
		}
	}, [chatMessages]);

	const stopCountdown = () => {
		setLoading(false);
	};

	const [nrVideosToFetch, setNrVideosToFetch] = useState(6);
	const [offsetNrVideosToFetch, setOffsetNrVideosToFetch] = useState(0);
	const [offsetVideoLinks, setOffsetVideoLinks] = useState([]);
	const handleSubmit = async () => {
		console.log(
			"nrVideosToFetch",
			nrVideosToFetch,
			"offsetNrVideosToFetch",
			offsetNrVideosToFetch
		);
		const agencyInfo = {
			agency_name: agencyName,
			agency_description: agencyDescription,
			industry,
			location,
			keywords,
			target_audience: targetAudience,
		};
		startCountdown();
		try {
			const response = await fetch(
				baseUrl +
					"/collect/videos?n=" +
					nrVideosToFetch +
					"&offset=" +
					offsetNrVideosToFetch,
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						agency_info: agencyInfo,
					}),
				}
			);

			if (response.ok) {
				const data = await response.json();
				if (data === null) {
					throw new Error("No videos found");
				}
				stopCountdown();
				setVideoResults((prevResults) => ({
					videos: [
						...data.videos,
						...(prevResults ? prevResults.videos : []),
					],
				}));
				setVideoSelected(new Array(data.videos.length).fill(false));
				console.log("Success:", data);
			} else {
				stopCountdown();
				console.error("Error:", response.statusText);
			}
		} catch (error) {
			stopCountdown();
			console.error("Network error:", error);
		}
	};

	// Toggle video selection
	const toggleSelection = (index) => {
		setVideoSelected((prevSelected) => {
			const newSelected = [...prevSelected];
			newSelected[index] = !newSelected[index];
			return newSelected;
		});
	};

	const sendMessage = async (message) => {
		setLoading(true);
		const currentMessages = chatMessages;
		setChatMessages((prevMessages) => [
			...prevMessages,
			{
				role: "user",
				content: message,
			},
			{
				role: "assistant",
				content: "💬 ..",
			},
		]);
		setUserInput("");

		// call the backend to get the response
		try {
			const videosToSend = videoResults;
			if (uploadedFile) {
				videosToSend.push({
					link: uploadedFile,
					relevancy_score: uploadResults["relevancy_score"],
					video_context: uploadResults["video_context"],
					audio_context: uploadResults["audio_context"],
					text_content: "User uploaded video",
				});
			}

			const response = await fetch(baseUrl + "/chat", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					message_history: {
						message_history: currentMessages,
						user_input: message,
					},
					agency_info: {
						agency_name: agencyName,
						agency_description: agencyDescription,
						industry,
						location,
						keywords,
						target_audience: targetAudience,
						videos_selected: videosToSend,
					},
				}),
			});

			if (response.ok) {
				const data = await response.json();
				if (data === null) {
					throw new Error("No videos found");
				}
				stopCountdown();
				setChatMessages(data);
				console.log("Success:", data);
			} else {
				stopCountdown();
				console.error("Error:", response.statusText);
			}
		} catch (error) {
			stopCountdown();
			console.error("Network error:", error);
		}
	};

	const resetChat = () => {
		// Confirm dialog
		setOpen(false);
		setChatMessages(welcomeMessage);
	};

	const startChat = () => {
		const selectedVideos = videoResults.videos.filter(
			(_, idx) => videoSelected[idx]
		);
		setVideoResults({ videos: selectedVideos });
		setVideoSelected(new Array(selectedVideos.length).fill(true));
		setChatState(true);
	};

	// // Replace '\n' with double spaces (for Markdown interpretation)
	// const formatMessageForMarkdown = (messageContent) => {
	// 	console.log("messageContent", messageContent);
	// 	try {
	// 		console.log(1);
	// 		const finalmessage = messageContent.replace(/\n/g, "&nbsp;  ");
	// 		console.log("finalmessage", finalmessage);
	// 		return finalmessage;
	// 	} catch (e) {
	// 		console.log("error", e);
	// 		return messageContent;
	// 	}
	// };

	const [timesShuffled, setTimesShuffled] = useState(1);
	const reshuffleVideos = () => {
		const selectedVideos = videoResults.videos.filter(
			(_, idx) => videoSelected[idx]
		);

		setVideoResults({ videos: selectedVideos });
		const newLength = selectedVideos.length;
		console.log("newLength", newLength);
		setNrVideosToFetch(6 - newLength);
		setOffsetVideoLinks(selectedVideos.map((video) => video.link));
		setTimesShuffled(timesShuffled + 1);
		setVideoSelected(new Array(newLength).fill(true));
		setOffsetNrVideosToFetch(6 * timesShuffled + (6 - newLength));
	};

	useEffect(() => {
		if (nrVideosToFetch !== 6 || offsetNrVideosToFetch !== 0) {
			handleSubmit();
		}
	}, [nrVideosToFetch, offsetNrVideosToFetch]);

	const [uploadedFile, setUploadedFile] = useState(null);
	const [uploadedFileUrl, setUploadedFileUrl] = useState(null);

	useEffect(() => {
		if (!uploadedFile) return;

		const uploadVideo = async () => {
			try {
				const formData = new FormData();
				formData.append("video_file", uploadedFile);

				const response = await fetch(`${baseUrl}/video/analysis`, {
					method: "POST",
					body: formData,
				});

				if (!response.ok) {
					throw new Error(`HTTP error! Status: ${response.status}`);
				}

				const result = await response.json();

				const results = {
					relevancy_score: "Not available",
					video_context: result.output,
					audio_context: "",
					text_context: "User uploaded video",
				};

				setUploadResults(results);
			} catch (error) {
				console.error("Error:", error);
			}
		};

		uploadVideo();

		// Cleanup when the file changes or component unmounts
		return () => {
			setUploadResults(null);
		};
	}, [uploadedFile, baseUrl]);

	const removeFile = () => {
		setUploadedFile(null);
		setUploadResults(null);
		setUploadedFileUrl(null);
	};

	const handleFileUpload = (file) => {
		setUploadedFile(file);
		setUploadedFileUrl(URL.createObjectURL(file));
	};
	return (
		<div className="bg-[#454343] h-screen w-screen px-[30px] py-[35px]">
			<h1 className="text-xl text-white absolute ml-[30px] top-0 left-0">
				Video Recommendation System
			</h1>
			<button
				className="p-1 text-sm bg-slate-300 rounded-md  hover:bg-slate-400 text-slate-600 absolute top-0 right-0 mr-[30px] mt-1"
				onClick={() => window.location.reload()}
			>
				Restart
			</button>
			<div className="gap-4 rounded-md h-full w-full hover:shadow-xl flex bg-[#241f1f] px-3 ">
				{!videoResults && (
					<div className="flex flex-col text-center space-y-5 justify-center my-3 py-5 w-1/2 p-5 border rounded-md border-white">
						<h1 className="text-center text-white text-2xl">
							Step 1: Agency Info
						</h1>
						<p className="!mb-20">
							Your agency information will be used to get 3 videos
							that align with your agency's brand and target
							audience.
						</p>
						<div className="!mt-10 w-4/6 flex flex-col justify-center mx-auto">
							{counter === 0 && (
								<input
									type="text"
									placeholder="Agency Name"
									className="p-5 rounded-md text-slate-600"
									value={agencyName}
									onChange={(e) =>
										setAgencyName(e.target.value)
									}
								/>
							)}
							{counter === 1 && (
								<input
									type="text"
									placeholder="Describe your agency in one sentence"
									className="p-5 rounded-md text-slate-600"
									value={agencyDescription}
									onChange={(e) =>
										setAgencyDescription(e.target.value)
									}
								/>
							)}
							{counter === 2 && (
								<input
									type="text"
									placeholder="Industry"
									className="p-5 rounded-md text-slate-600"
									value={industry}
									onChange={(e) =>
										setIndustry(e.target.value)
									}
								/>
							)}
							{counter === 3 && (
								<input
									type="text"
									placeholder="Location"
									className="p-5 rounded-md text-slate-600"
									value={location}
									onChange={(e) =>
										setLocation(e.target.value)
									}
								/>
							)}
							{counter === 4 && (
								<input
									type="text"
									placeholder="Keywords (separated by commas)"
									className="p-5 rounded-md text-slate-600"
									value={keywords}
									onChange={(e) =>
										setKeywords(e.target.value)
									}
								/>
							)}
							{counter === 5 && (
								<input
									type="text"
									placeholder="Target Audience"
									className="p-5 rounded-md text-slate-600"
									value={targetAudience}
									onChange={(e) =>
										setTargetAudience(e.target.value)
									}
								/>
							)}
							<div className="flex justify-between pt-10 w-3/4 mx-auto">
								{counter > 0 && !loading && (
									<button
										onClick={() => setCounter(counter - 1)}
										className="p-5 text-2xl bg-slate-200 rounded-md w-[150px] hover:bg-slate-400 text-slate-600"
									>
										Previous
									</button>
								)}
								{counter < 5 && (
									<button
										onClick={() => setCounter(counter + 1)}
										className="p-5 text-2xl bg-slate-300 ml-auto rounded-md w-[150px] hover:bg-slate-400 text-slate-600"
									>
										Next
									</button>
								)}
								{counter === 5 && !loading && (
									<button
										className="p-5 text-2xl bg-blue-300 rounded-md rounded-md w-[150px] hover:bg-slate-400 text-slate-600"
										onClick={handleSubmit}
										disabled={loading}
									>
										Submit
									</button>
								)}
							</div>
						</div>
					</div>
				)}
				{videoResults && !chatState && (
					<div className="flex flex-col text-center space-y-5 justify-center my-3 py-5 w-1/2 p-5 border rounded-md border-white">
						<h1 className="text-center text-white text-2xl">
							Step 2: Video Selection
						</h1>
						<p className="!mb-20">
							Select 3 videos of your preference or reshuflle the
							list.
						</p>
						<p className="text-white text-xl">
							Selected Videos:{" "}
							{
								videoSelected.filter((selected) => selected)
									.length
							}
						</p>
						<div className="!mt-10 w-4/6 flex justify-between pt-10 w-1/2 mx-auto">
							<button
								className={`p-5 text-xl bg-slate-200 rounded-md w-[150px] ${
									videoSelected.filter((selected) => selected)
										.length >= 3
										? "hover:bg-slate-400"
										: "bg-slate-400"
								} text-slate-600`}
								disabled={
									videoSelected.filter((selected) => selected)
										.length < 3
								}
								onClick={() => startChat()}
							>
								Chat
							</button>
							<button
								className="p-5 text-xl bg-slate-200 rounded-md w-[150px] hover:bg-slate-400 text-slate-600"
								onClick={() => reshuffleVideos()}
								disabled={
									loading ||
									videoSelected.filter((selected) => selected)
										.length >= 3
								}
							>
								Reshuffle
							</button>
						</div>
					</div>
				)}
				{videoResults && chatState && (
					<div className="flex flex-col text-center space-y-5 justify-center my-3 py-5 w-1/2 p-5 border rounded-md border-white">
						<div className="flex flex-col gap-5 bg-slate-300 p-5 rounded-md w-full h-full">
							<div
								className="flex flex-col space-y-10 overflow-y-auto h-full w-full"
								id="chatWindow"
								ref={chatWindowRef}
							>
								{chatMessages.map(
									(message, index) =>
										(message.role === "user" ||
											message.role === "assistant") && (
											<div
												key={index}
												className={`flex gap-5 items-end ${
													message.role === "user"
														? "flex-row-reverse"
														: ""
												}`}
											>
												<div className="shadow-md bg-slate-200 rounded-full w-10 h-10 flex items-center justify-center">
													<span>
														{message.role ===
														"assistant"
															? "🤖"
															: "🧑‍💻"}
													</span>
												</div>
												<div
													className={`flex flex-col space-y-5 w-3/4 ${
														message.role ===
														"assistant"
															? "items-start"
															: "items-end"
													}`}
												>
													<div
														className={`px-5 py-3 rounded-md max-w-full text-start shadow-md ${
															message.role ===
															"assistant"
																? "bg-slate-200 text-slate-600"
																: "bg-sky-950 text-slate-200"
														}`}
													>
														<ReactMarkdown className="whitespace-break-spaces">
															{message.content}
														</ReactMarkdown>
													</div>
												</div>
											</div>
										)
								)}
							</div>
							<div
								className="flex w-full gap-5 items-center"
								id="chatInput"
							>
								<input
									type="text"
									value={userInput}
									onChange={(e) =>
										setUserInput(e.target.value)
									}
									placeholder="Type a message.."
									className="p-2 rounded-md text-slate-600 w-full"
									onKeyDown={(e) => {
										if (e.key === "Enter") {
											sendMessage(e.target.value);
										}
									}}
								/>

								<Tooltip title="Focus Group">
									<button
										className="p-2 text-xl bg-slate-200 rounded-md w-[150px] hover:bg-slate-400 text-slate-600"
										disabled={loading}
									>
										<InterpreterModeIcon
											onClick={() =>
												sendMessage(
													"Please evaluate the selected videos via the Focus Group"
												)
											}
										/>
									</button>
								</Tooltip>
								<Tooltip title="Restore Chat">
									<button
										className="p-2 text-xl bg-slate-200 rounded-md w-[150px] hover:bg-slate-400 text-slate-600"
										disabled={loading}
									>
										<RestoreIcon
											onClick={() => handleResetChat()}
										/>
									</button>
								</Tooltip>
								<React.Fragment>
									<Dialog
										open={open}
										onClose={handleClose}
										aria-labelledby="alert-dialog-title"
										aria-describedby="alert-dialog-description"
									>
										<DialogTitle id="alert-dialog-title">
											{"Reset?"}
										</DialogTitle>
										<DialogContent>
											<DialogContentText id="alert-dialog-description">
												Do you want to reset this chat?
											</DialogContentText>
										</DialogContent>
										<DialogActions>
											<Button onClick={handleClose}>
												No
											</Button>
											<Button
												onClick={resetChat}
												autoFocus
											>
												Yes
											</Button>
										</DialogActions>
									</Dialog>
								</React.Fragment>
								<Tooltip title="Send message">
									<button
										className="p-2 text-xl bg-slate-200 rounded-md w-[150px] hover:bg-slate-400 text-slate-600"
										disabled={loading}
									>
										<SendIcon
											onClick={() =>
												sendMessage(userInput)
											}
										/>
									</button>
								</Tooltip>
							</div>
						</div>
					</div>
				)}
				<div className="flex flex-col text-center space-y-5 justify-center border rounded-md border-white  my-3 w-1/2 p-5">
					{((!videoResults && !loading) || loading) && (
						<img
							src={logo}
							className={`w-[50px] h-[50px] mx-auto ${
								loading ? "App-logo" : ""
							}`}
							alt="logo"
						/>
					)}
					{loading &&
						videoSelected.filter((selected) => selected).length <
							3 && (
							<div>
								<h1 className="text-white text-2xl">
									{loadingMessages[messageCounter]}
								</h1>
								<small>
									{timeLeft > 0
										? "Estimated time left: " +
										  timeLeft +
										  "s"
										: ""}
								</small>
							</div>
						)}

					{videoResults && (
						<div className="flex flex-wrap gap-10 overflow-y-auto">
							{videoResults.videos.map((video, index) => (
								<div
									key={index}
									className={`flex flex-col w-[350px] space-y-5 p-5 bg-gray-800 rounded-md ${
										videoSelected[index]
											? "border-2 border-blue-400"
											: "border border-white"
									}`}
								>
									<Switch
										checked={videoSelected[index]}
										onChange={() => toggleSelection(index)}
										className="ml-auto"
										disabled={
											chatState ||
											videoSelected.filter(
												(selected) => selected
											).length >= 3
										}
									/>
									<video
										controls
										className="w-full max-h-[200px] rounded-md"
										src={video.link}
									></video>
									<small className="font-bold">
										Relevancy Score:{" "}
										<span className="font-normal">
											{video.relevancy_score}
										</span>
									</small>
									<Accordion>
										<AccordionSummary
											expandIcon={<ArrowDownwardIcon />}
											aria-controls="panel1-content"
											id="panel1-header"
										>
											<Typography>
												More details
											</Typography>
										</AccordionSummary>
										<AccordionDetails>
											<div className="text-left flex flex-col space-y-5">
												<small className="font-bold">
													Video:{" "}
													<span className="font-normal">
														{video.video_context}
													</span>
												</small>
												<small className="font-bold">
													Audio:{" "}
													<span className="font-normal">
														{video.audio_context}
													</span>
												</small>
											</div>
										</AccordionDetails>
									</Accordion>
								</div>
							))}
							{chatState &&
								videoSelected.filter((selected) => selected)
									.length === 3 &&
								!uploadResults && (
									<Button
										component="label"
										role={undefined}
										variant="contained"
										tabIndex={-1}
										startIcon={<CloudUploadIcon />}
										className="w-[350px] h-auto rounded-md"
									>
										Upload a Video of your own
										<VisuallyHiddenInput
											type="file"
											onChange={(event) =>
												handleFileUpload(
													event.target.files[0]
												)
											}
											accept="video/*"
										/>
									</Button>
								)}
							{chatState && uploadResults && (
								<div className="flex flex-col w-[350px] space-y-5 p-5 bg-gray-800 rounded-md border-2 border-green-200">
									<div className="flex items-center justify-between">
										<CloseIcon
											onClick={() => removeFile()}
										/>
										<Switch
											checked={true}
											className="ml-auto"
											disable={true}
										/>
									</div>
									<video
										controls
										className="w-full max-h-[200px] rounded-md"
										src={uploadedFileUrl}
									></video>
									<small className="font-bold">
										Relevancy Score:{" "}
										<span className="font-normal">
											{uploadResults.relevancy_score}
										</span>
									</small>
									<Accordion>
										<AccordionSummary
											expandIcon={<ArrowDownwardIcon />}
											aria-controls="panel1-content"
											id="panel1-header"
										>
											<Typography>
												More details
											</Typography>
										</AccordionSummary>
										<AccordionDetails>
											<div className="text-left flex flex-col space-y-5">
												<small className="font-bold">
													Video:{" "}
													<span className="font-normal">
														{
															uploadResults.video_context
														}
													</span>
												</small>
												<small className="font-bold">
													Audio:{" "}
													<span className="font-normal">
														{
															uploadResults.audio_context
														}
													</span>
												</small>
											</div>
										</AccordionDetails>
									</Accordion>
								</div>
							)}
						</div>
					)}
				</div>
			</div>
		</div>
	);
}

export default App;
