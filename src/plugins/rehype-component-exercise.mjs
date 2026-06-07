/// <reference types="mdast" />
import { h } from "hastscript";

function splitDirectiveLabel(properties, children) {
	if (!Array.isArray(children) || children.length === 0) {
		return { label: null, content: [] };
	}

	if (!properties?.["has-directive-label"]) {
		return { label: null, content: children };
	}

	const [label, ...content] = children;
	label.tagName = "span";
	label.properties = {
		...(label.properties || {}),
		className: ["bdm-label"],
	};

	return { label, content };
}

/**
 * Creates a problem block.
 *
 * @param {Object} properties - The directive properties.
 * @param {import('mdast').RootContent[]} children - The children elements.
 * @returns {import('mdast').Parent} The created problem component.
 */
export function ProblemComponent(properties, children) {
	const { label, content } = splitDirectiveLabel(properties, children);
	if (content.length === 0) {
		return h(
			"div",
			{ class: "hidden" },
			'Invalid problem directive. (Use ":::problem[title] <content> :::")',
		);
	}

	return h("blockquote", { class: "admonition exercise-block bdm-problem" }, [
		h("span", { class: "bdm-title" }, label || "题目"),
		...content,
	]);
}

/**
 * Creates a collapsible solution block.
 *
 * @param {Object} properties - The directive properties.
 * @param {import('mdast').RootContent[]} children - The children elements.
 * @returns {import('mdast').Parent} The created solution component.
 */
export function SolutionComponent(properties, children) {
	const { label, content } = splitDirectiveLabel(properties, children);
	if (content.length === 0) {
		return h(
			"div",
			{ class: "hidden" },
			'Invalid solution directive. (Use ":::solution[title] <content> :::")',
		);
	}

	return h("details", { class: "admonition exercise-block bdm-solution" }, [
		h("summary", { class: "bdm-title" }, label || "题解"),
		h("div", { class: "bdm-content" }, content),
	]);
}
