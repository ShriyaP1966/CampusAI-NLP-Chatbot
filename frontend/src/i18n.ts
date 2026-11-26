import type { AnswerLanguage, ApiErrorKind } from './api';

export interface Strings {
  tagline: string;
  sampleNotice: string;
  language: string;
  autoDetect: string;
  inputLabel: string;
  inputHint: string;
  send: string;
  sending: string;
  clear: string;
  thinking: string;
  you: string;
  assistant: string;
  sources: (count: number) => string;
  emptyTitle: string;
  emptyBody: string;
  suggestedTitle: string;
  retry: string;
  refusedLabel: string;
  notFoundLabel: string;
  wakingTitle: string;
  wakingBody: string;
  unavailableTitle: string;
  unavailableBody: string;
  waitingForServer: string;
  errors: Record<ApiErrorKind, string>;
}

const en: Strings = {
  tagline: 'Ask about admissions, courses, fees, exams, scholarships, events and more.',
  sampleNotice:
    'Answers come from sample documents of a fictional university. They are not real college information.',
  language: 'Language',
  autoDetect: 'Auto-detect',
  inputLabel: 'Your question',
  inputHint: 'Press Enter to send',
  send: 'Send',
  sending: 'Sending',
  clear: 'Clear chat',
  thinking: 'Looking through the documents',
  you: 'You',
  assistant: 'CampusAI',
  sources: (count) => (count === 1 ? '1 source' : `${count} sources`),
  emptyTitle: 'What would you like to know?',
  emptyBody: 'Every answer shows the document it came from. If the answer is not in the documents, CampusAI says so.',
  suggestedTitle: 'Try asking',
  retry: 'Try again',
  refusedLabel: 'Request declined',
  notFoundLabel: 'Not in the documents',
  wakingTitle: 'Waking up the server',
  wakingBody:
    'The free server sleeps when nobody uses it. This can take up to a minute the first time. You can already type your question.',
  unavailableTitle: 'The server is not responding',
  unavailableBody: 'It may still be starting. Please try again in a moment.',
  waitingForServer: 'Waiting for the server',
  errors: {
    config: 'The app is not connected to a backend. Set VITE_API_URL and rebuild.',
    network: 'Could not reach the server. Check your connection and try again.',
    timeout: 'The server took too long to answer. It may be waking up. Please try again.',
    rate_limit: 'Too many questions in a short time. Please wait a minute and try again.',
    invalid: 'That message could not be sent. Please shorten it and try again.',
    server: 'Something went wrong on the server. Please try again.',
  },
};

const hi: Strings = {
  ...en,
  tagline: 'प्रवेश, पाठ्यक्रम, शुल्क, परीक्षा, छात्रवृत्ति, कार्यक्रम और बहुत कुछ पूछें।',
  sampleNotice: 'उत्तर एक काल्पनिक विश्वविद्यालय के नमूना दस्तावेज़ों से आते हैं। यह किसी असली कॉलेज की जानकारी नहीं है।',
  language: 'भाषा',
  autoDetect: 'स्वतः पहचानें',
  inputLabel: 'आपका प्रश्न',
  inputHint: 'भेजने के लिए Enter दबाएँ',
  send: 'भेजें',
  sending: 'भेजा जा रहा है',
  clear: 'चैट साफ़ करें',
  thinking: 'दस्तावेज़ देखे जा रहे हैं',
  you: 'आप',
  sources: (count) => `${count} स्रोत`,
  emptyTitle: 'आप क्या जानना चाहते हैं?',
  emptyBody: 'हर उत्तर के साथ वह दस्तावेज़ दिखता है जिससे वह लिया गया है। यदि उत्तर दस्तावेज़ों में नहीं है, तो CampusAI यह बता देता है।',
  suggestedTitle: 'ये पूछकर देखें',
  retry: 'फिर कोशिश करें',
  refusedLabel: 'अनुरोध स्वीकार नहीं किया गया',
  notFoundLabel: 'दस्तावेज़ों में नहीं मिला',
  wakingTitle: 'सर्वर चालू हो रहा है',
  wakingBody: 'मुफ़्त सर्वर उपयोग न होने पर सो जाता है। पहली बार इसमें एक मिनट तक लग सकता है। आप अपना प्रश्न अभी लिख सकते हैं।',
  unavailableTitle: 'सर्वर जवाब नहीं दे रहा',
  unavailableBody: 'हो सकता है वह अभी चालू हो रहा हो। कृपया थोड़ी देर बाद फिर कोशिश करें।',
  waitingForServer: 'सर्वर की प्रतीक्षा',
  errors: {
    config: 'ऐप किसी सर्वर से जुड़ा नहीं है। VITE_API_URL सेट करके फिर से बनाएँ।',
    network: 'सर्वर तक नहीं पहुँचा जा सका। अपना कनेक्शन जाँचें और फिर कोशिश करें।',
    timeout: 'सर्वर ने जवाब देने में बहुत समय लिया। हो सकता है वह चालू हो रहा हो। कृपया फिर कोशिश करें।',
    rate_limit: 'थोड़े समय में बहुत अधिक प्रश्न हो गए। कृपया एक मिनट रुककर फिर कोशिश करें।',
    invalid: 'यह संदेश भेजा नहीं जा सका। कृपया उसे छोटा करके फिर कोशिश करें।',
    server: 'सर्वर पर कुछ गड़बड़ हुई। कृपया फिर कोशिश करें।',
  },
};

const mr: Strings = {
  ...en,
  tagline: 'प्रवेश, अभ्यासक्रम, शुल्क, परीक्षा, शिष्यवृत्ती, कार्यक्रम आणि बरेच काही विचारा.',
  sampleNotice: 'उत्तरे एका काल्पनिक विद्यापीठाच्या नमुना कागदपत्रांतून येतात. ही कोणत्याही खऱ्या महाविद्यालयाची माहिती नाही.',
  language: 'भाषा',
  autoDetect: 'आपोआप ओळखा',
  inputLabel: 'तुमचा प्रश्न',
  inputHint: 'पाठवण्यासाठी Enter दाबा',
  send: 'पाठवा',
  sending: 'पाठवत आहे',
  clear: 'चॅट साफ करा',
  thinking: 'कागदपत्रे तपासली जात आहेत',
  you: 'तुम्ही',
  sources: (count) => `${count} स्रोत`,
  emptyTitle: 'तुम्हाला काय जाणून घ्यायचे आहे?',
  emptyBody: 'प्रत्येक उत्तरासोबत ते ज्या कागदपत्रातून घेतले ते दिसते. उत्तर कागदपत्रांत नसेल तर CampusAI तसे सांगतो.',
  suggestedTitle: 'हे विचारून पाहा',
  retry: 'पुन्हा प्रयत्न करा',
  refusedLabel: 'विनंती नाकारली',
  notFoundLabel: 'कागदपत्रांत सापडले नाही',
  wakingTitle: 'सर्व्हर सुरू होत आहे',
  wakingBody: 'मोफत सर्व्हर वापरला जात नसताना झोपी जातो. पहिल्यांदा एक मिनिटापर्यंत वेळ लागू शकतो. तुम्ही आताच तुमचा प्रश्न लिहू शकता.',
  unavailableTitle: 'सर्व्हर प्रतिसाद देत नाही',
  unavailableBody: 'तो कदाचित अजून सुरू होत असेल. कृपया थोड्या वेळाने पुन्हा प्रयत्न करा.',
  waitingForServer: 'सर्व्हरची प्रतीक्षा',
  errors: {
    config: 'अॅप कोणत्याही सर्व्हरशी जोडलेले नाही. VITE_API_URL सेट करून पुन्हा बनवा.',
    network: 'सर्व्हरपर्यंत पोहोचता आले नाही. तुमचे कनेक्शन तपासा आणि पुन्हा प्रयत्न करा.',
    timeout: 'सर्व्हरने उत्तर देण्यात खूप वेळ घेतला. तो कदाचित सुरू होत असेल. कृपया पुन्हा प्रयत्न करा.',
    rate_limit: 'थोड्या वेळात खूप प्रश्न झाले. कृपया एक मिनिट थांबून पुन्हा प्रयत्न करा.',
    invalid: 'हा संदेश पाठवता आला नाही. कृपया तो लहान करून पुन्हा प्रयत्न करा.',
    server: 'सर्व्हरवर काहीतरी चूक झाली. कृपया पुन्हा प्रयत्न करा.',
  },
};

export const STRINGS: Record<AnswerLanguage, Strings> = { en, hi, mr };

export const LANGUAGE_OPTIONS: { value: 'auto' | AnswerLanguage; label: string }[] = [
  { value: 'auto', label: 'Auto-detect' },
  { value: 'en', label: 'English' },
  { value: 'hi', label: 'हिन्दी' },
  { value: 'mr', label: 'मराठी' },
];
