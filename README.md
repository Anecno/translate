# Translate
Suitable for translation tasks where there is no deadline pressure and high-quality
is the priority. Not suitable for translating long texts; performance is better with just a few paragraphs.

## Notes

1. This is a skill I use for my own work. If you intend to reuse it, please adapt it to your own circumstances and constraints.

2. The project includes several safeguard files designed to keep AI systems from skipping important steps. Unless you have a stronger way to keep those steps visible and enforceable, I recommend keeping these files and adapting them to your own workflow.

3. Deep-research methods are described only briefly. You may use more flexible approaches where appropriate.

4. In my own workflow, I have largely moved away from direct CLI calls. Instead, I use Claude Code to write the prompts, and then I relay them myself through our current default relay chain: a fixed, serial hand-off across five models. The first baton (which specializes in looking up target-language dictionaries through NotebookLM) produces the initial rendering; three strong models in the middle each review and revise it in turn; and the fifth baton (which is equipped with web access and is used specifically to dig into the source- and target-language sites that other AIs can't easily reach) closes the chain. NotebookLM has strict token limits; sending a very long prompt might cause it to crash. It is recommended to either compress the prompt or upload the prompt file to NotebookLM (recommended) for processing.

   There are three reasons for this workflow. First, this combination lets me draw on the complementary strengths of large language models, dictionaries, and web resources all at once. Second, this workflow is more transparent: I can inspect the prompt directly and revise it before sending it. Third, high-quality translation cannot be achieved by asking a large language model to produce a final answer in one pass. What I would call the external entropy of human thought — human judgment, disagreement, revision, and interpretive friction — is especially important.

   As the repository description suggests, this project is best suited to users who have enough time to weigh words carefully. It is also better suited to users who are fluent in at least one foreign language and do not need to rely on the skill as a black-box translator. Multilingual input and the workflow outputs can both preserve traces of human external entropy, helping calibrate the direction of translation. In one past project, reading the divergent-analysis output allowed me to manually synthesize the translation I wanted most.

5. Reference standards, research directions, and reviewed GitHub projects are listed in [`translate-v2/REFERENCES.md`](./translate-v2/REFERENCES.md). Dictionary references used in NotebookLM are listed in [`Dictionary-References.md`](./Dictionary-References.md). The web-access capability used by the fifth baton comes from the open-source [web-access](https://github.com/eze-is/web-access) skill by eze-is (MIT License).
