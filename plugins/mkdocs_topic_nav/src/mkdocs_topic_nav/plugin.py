from copy import deepcopy
from typing import Any

from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation, Page, Section

TOPIC_SECTIONS = ["Developer Environment", "Software Products"]


class TopicNavPlugin(BasePlugin):
    """Hide internals of topics in the navigation panel."""

    def on_page_context(self, context: dict[str, Any], page: Page, config, nav: Navigation, **kwargs):
        if page.title in TOPIC_SECTIONS:
            context["nav"] = self._filter_section_nav(nav)
        elif any(s.title in TOPIC_SECTIONS for s in page.ancestors):
            context["nav"] = self._filter_topic_nav(nav, page)

        return context

    @staticmethod
    def _filter_section_nav(nav: Navigation):
        new_nav = deepcopy(nav)
        for item in new_nav.items:
            if isinstance(item, Section) and item.title in TOPIC_SECTIONS:
                for topic in item.children:
                    if isinstance(topic, Section):
                        topic.children = [
                            p
                            for p in topic.children
                            if isinstance(p, Page) and p.is_index
                        ]

        return new_nav

    @staticmethod
    def _filter_topic_nav(nav: Navigation, page: Page):
        root_section = page.ancestors[-1]
        topic_section = page.ancestors[-2]

        new_nav = deepcopy(nav)
        for item in new_nav.items:
            if item.title == root_section.title:
                item.children = [
                    i
                    for i in item.children
                    if isinstance(i, Page) or i.title == topic_section.title
                ]

        return new_nav
