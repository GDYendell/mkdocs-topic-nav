from copy import deepcopy
from typing import Any

from mkdocs.plugins import BasePlugin
from mkdocs.structure.nav import Navigation, Page, Section

ROOT_SECTIONS = ["Developer Environment", "Software Products"]


class TopicNavPlugin(BasePlugin):
    """Hide internals of topics in the navigation panel.

    This plugin assumes that navigation.tabs and navigation.indexes are enabled so that
    the root sections are level 2 nested and when inside one it is rendered as the
    header of the nav with the topics at the root. It is recommended to use
    navigation.expand so that when entering a topic the full tree is displayed. The
    navigation.sections feature can either be enabled or disabled to modify the
    appearance of the topic titles in the nav.

    """

    def on_page_context(
        self, context: dict[str, Any], page: Page, config, nav: Navigation, **kwargs
    ):
        """Hook called by mkdocs when rendering a specific page."""
        if page.title in ROOT_SECTIONS:
            # This page a root section index
            context["nav"] = self._filter_section_nav(nav)
        elif any(s.title in ROOT_SECTIONS for s in page.ancestors):
            # This page is a topic section index (or child of a section index)
            # Only display this topic and its child pages
            context["nav"] = self._filter_topic_nav(nav, page)

        return context

    @staticmethod
    def _filter_section_nav(nav: Navigation):
        """Filter nav to this section and its topic indexes without their children."""

        new_nav = deepcopy(nav)
        for item in new_nav.items:
            if isinstance(item, Section) and item.title in ROOT_SECTIONS:
                # This is the a root section within the nav panel
                for topic in item.children:
                    if isinstance(topic, Section):
                        # This is a topic section
                        # Filter nav to display only the index page of the topic
                        topic.children = [
                            p
                            for p in topic.children
                            if isinstance(p, Page) and p.is_index
                        ]

        return new_nav

    @staticmethod
    def _filter_topic_nav(nav: Navigation, page: Page):
        """Filter nav to this topic and its child pages."""

        root_section = page.ancestors[-1]
        topic_section = page.ancestors[-2]

        new_nav = deepcopy(nav)
        for item in new_nav.items:
            if item.title == root_section.title:
                # This is the topic section containing the topic for the current page
                # Filter nav to only display this topic section and its pages
                item.children = [
                    i
                    for i in item.children
                    if i.title == topic_section.title or isinstance(i, Page)
                ]

        return new_nav
