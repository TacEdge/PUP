// Placeholder leadership feedback instrument.
//
// This is provisional developmental content for prototyping the product. It is
// NOT NZ Army doctrine and must not be presented as the approved NZALC
// framework. The application reads this file as data: replace the dimensions,
// statements and prompts here and every screen updates without UI changes.

export const instrument = {
  id: "proto-v1",
  name: "Leadership feedback (prototype instrument)",
  estimatedMinutes: 4,

  // Rating scale. `value` feeds averages; `null` is excluded from them.
  scale: [
    { key: "rarely", label: "Rarely", value: 1, hotkey: "1" },
    { key: "sometimes", label: "Sometimes", value: 2, hotkey: "2" },
    { key: "usually", label: "Usually", value: 3, hotkey: "3" },
    { key: "consistently", label: "Consistently", value: 4, hotkey: "4" },
  ],
  notObserved: { key: "not_observed", label: "Not observed", value: null, hotkey: "n" },

  dimensions: [
    {
      id: "self",
      name: "Leads Self",
      short: "Self",
      statements: [
        { id: "s1", text: "Remains composed under pressure." },
        { id: "s2", text: "Shows awareness of how their behaviour affects others." },
        { id: "s3", text: "Accepts feedback and acts on it." },
        { id: "s4", text: "Acts consistently with the values they state." },
      ],
    },
    {
      id: "others",
      name: "Leads Others",
      short: "Others",
      statements: [
        { id: "o1", text: "Communicates clearly and directly." },
        { id: "o2", text: "Builds trust with the people they work with." },
        { id: "o3", text: "Takes an active interest in developing others." },
        { id: "o4", text: "Creates an environment where people are willing to speak up." },
      ],
    },
    {
      id: "teams",
      name: "Leads Teams",
      short: "Teams",
      statements: [
        { id: "t1", text: "Provides clear direction and priorities." },
        { id: "t2", text: "Makes timely decisions when they are needed." },
        { id: "t3", text: "Builds cohesion across the team." },
        { id: "t4", text: "Holds the team, and themselves, to appropriate standards." },
      ],
    },
    {
      id: "adapts",
      name: "Adapts & Learns",
      short: "Adapts",
      statements: [
        { id: "a1", text: "Adjusts their approach when circumstances change." },
        { id: "a2", text: "Learns from experience, including mistakes." },
        { id: "a3", text: "Seeks out perspectives different from their own." },
      ],
    },
  ],

  // Short written prompts asked once, at the end. Two only, by design.
  prompts: [
    {
      id: "keep",
      heading: "Keep doing",
      question: "What should {first} keep doing?",
      hint: "One or two sentences is plenty.",
      optional: false,
    },
    {
      id: "more",
      heading: "More effective",
      question: "What could {first} do to be more effective?",
      hint: "Specific beats polished. One or two sentences.",
      optional: false,
    },
  ],
};

// Rater relationships. `anonymised` groups are reported only when the group
// reaches `minGroupSize`; superiors are reported as a group of any size and
// are told so before they begin.
export const relationships = [
  { key: "self", label: "Self", plural: "Self", anonymised: false },
  { key: "superior", label: "Superior", plural: "Superiors", anonymised: false },
  { key: "peer", label: "Peer", plural: "Peers", anonymised: true },
  { key: "subordinate", label: "Subordinate", plural: "Subordinates", anonymised: true },
  { key: "other", label: "Other", plural: "Others", anonymised: true },
];

export const privacy = {
  minGroupSize: 3,
  pooledGroupLabel: "Other raters",
};

export const allStatements = () =>
  instrument.dimensions.flatMap((d) => d.statements.map((s) => ({ ...s, dimensionId: d.id })));
