# StarHTML Slot System — Reference

## Contents
- [What slots are](#what-slots-are)
- [Defining slots in a component](#defining-slots-in-a-component)
- [Using a component with slots](#using-a-component-with-slots)
- [Passing attributes vs content](#passing-attributes-vs-content)
- [Complete examples](#complete-examples)

---

## What slots are

Slots allow component authors to expose named injection points. Consumers can pass content or reactive attributes to specific parts of a component without knowing its internal DOM structure.

Without slots, customizing a reusable component requires modifying its internals or passing everything as props. With slots, you define named areas and let consumers fill them.

---

## Defining slots in a component

    def Modal(body_content, **kwargs):
        return Div(
            # data_slot marks an injection point with a name
            Div(data_slot="header"),
            Div(body_content, data_slot="body"),
            Div(data_slot="footer"),

            # slot_<name>=dict(...) applies attributes reactively to that slot
            slot_header=dict(
                cls="modal-header",
                data_show=show_header,          # reactive attribute on header slot
            ),
            slot_body=dict(
                data_attr_class=expanded.if_("modal-body-expanded", "modal-body"),
            ),
            slot_footer=dict(
                data_show=has_actions,
                style="display:none",           # flash prevention
            ),

            cls="modal",
            **kwargs   # always include **kwargs to allow pass-through attributes
        )

**Rules for component authors:**
- Always include `**kwargs` in the function signature
- Add `style="display:none"` to slots that use `data_show`
- Use `slot_<name>=dict(...)` for reactive attributes on slots
- Slot names must be valid Python identifiers (use underscores, not hyphens)

---

## Using a component with slots

    # Pass content to slots via slot_<name>=Element(...)
    Modal(
        "Main body text here",              # positional → body_content parameter

        slot_header=Div(
            H2("Modal Title"),
            Button("×", cls="close-btn"),
            cls="modal-header-content"
        ),
        slot_footer=Div(
            Button("Cancel", cls="btn btn-secondary"),
            Button("Confirm", cls="btn btn-primary"),
        ),

        id="my-modal",
        cls="modal-lg"
    )

---

## Passing attributes vs content

Two different uses of `slot_<name>`:

    # Pass ATTRIBUTES to a slot (dict) — adds reactive behavior
    slot_header=dict(
        data_show=is_authenticated,
        data_attr_class=is_admin.if_("admin-header", "user-header"),
    )

    # Pass CONTENT to a slot (Element) — replaces the slot's children
    slot_header=Div(H2("Title"), Button("×"))

    # Slots without any content passed remain as defined in the component

---

## Complete examples

### Card component

    def Card(body_content, **kwargs):
        return Div(
            Div(data_slot="header", cls="card-header"),
            Div(body_content, data_slot="body", cls="card-body"),
            Div(data_slot="footer", cls="card-footer"),

            slot_footer=dict(
                data_show=has_footer_content,
                style="display:none",
            ),

            cls="card",
            **kwargs
        )

    # Usage
    Card(
        P("Card body text goes here."),
        slot_header=H3("Card Title"),
        slot_footer=Button("Primary Action", cls="btn btn-primary"),
        id="my-card",
        cls="shadow-md"
    )

### Sidebar layout

    def Sidebar(main_content, **kwargs):
        return Div(
            Nav(data_slot="nav", cls="sidebar-nav"),
            Main(main_content, data_slot="main", cls="main-content"),

            slot_nav=dict(
                data_attr_class=is_collapsed.if_("nav-collapsed", "nav-expanded"),
            ),

            cls="sidebar-layout",
            **kwargs
        )

    # Usage
    Sidebar(
        Div("Page content here"),
        slot_nav=Ul(
            Li(A("Home", href="/")),
            Li(A("Settings", href="/settings")),
        ),
    )
