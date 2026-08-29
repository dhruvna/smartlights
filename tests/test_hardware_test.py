import pytest

from smartlights.color import RGB
from smartlights.hardware_test import (
    DiagnosticMode,
    build_diagnostic_steps,
    create_parser,
    main,
    partial_solid_frame,
    pixel_range_frame,
    single_pixel_frame,
)


def test_partial_frame_only_lights_requested_pixels() -> None:
    color = RGB(10, 20, 30)

    assert partial_solid_frame(
        color=color,
        pixel_count=5,
        active_pixel_count=2,
    ) == (
        color,
        color,
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 0),
    )


def test_partial_frame_allows_zero_active_pixels() -> None:
    assert partial_solid_frame(
        color=RGB(10, 20, 30),
        pixel_count=3,
        active_pixel_count=0,
    ) == (
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 0),
    )


def test_partial_frame_rejects_invalid_pixel_count() -> None:
    with pytest.raises(
        ValueError,
        match="Pixel count must be greater than zero",
    ):
        partial_solid_frame(
            color=RGB(10, 20, 30),
            pixel_count=0,
            active_pixel_count=0,
        )


def test_partial_frame_rejects_too_many_active_pixels() -> None:
    with pytest.raises(
        ValueError,
        match="Active pixel count must be between",
    ):
        partial_solid_frame(
            color=RGB(10, 20, 30),
            pixel_count=3,
            active_pixel_count=4,
        )


def test_partial_frame_rejects_negative_active_pixels() -> None:
    with pytest.raises(
        ValueError,
        match="Active pixel count must be between",
    ):
        partial_solid_frame(
            color=RGB(10, 20, 30),
            pixel_count=3,
            active_pixel_count=-1,
        )


def test_single_pixel_frame_only_lights_selected_pixel() -> None:
    color = RGB(10, 20, 30)

    assert single_pixel_frame(color, pixel_count=4, active_index=2) == (
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        color,
        RGB(0, 0, 0),
    )


def test_single_pixel_frame_rejects_out_of_range_index() -> None:
    with pytest.raises(ValueError, match="Active index must identify"):
        single_pixel_frame(RGB(10, 20, 30), pixel_count=3, active_index=3)


def test_pixel_range_frame_lights_half_open_range() -> None:
    color = RGB(10, 20, 30)

    assert pixel_range_frame(color, pixel_count=5, start_index=1, end_index=4) == (
        RGB(0, 0, 0),
        color,
        color,
        color,
        RGB(0, 0, 0),
    )


def test_pixel_range_frame_rejects_empty_range() -> None:
    with pytest.raises(ValueError, match="Pixel range must be within"):
        pixel_range_frame(RGB(10, 20, 30), pixel_count=5, start_index=2, end_index=2)


def test_channels_mode_builds_rgb_steps() -> None:
    steps = build_diagnostic_steps(
        mode=DiagnosticMode.CHANNELS,
        pixel_count=4,
        active_pixel_count=2,
        group_size=2,
    )

    assert len(steps) == 3
    assert steps[0].frame == (RGB(255, 0, 0), RGB(255, 0, 0), RGB(0, 0, 0), RGB(0, 0, 0))
    assert steps[1].frame[0] == RGB(0, 255, 0)
    assert steps[2].frame[0] == RGB(0, 0, 255)


def test_chase_mode_visits_every_pixel() -> None:
    steps = build_diagnostic_steps(
        mode=DiagnosticMode.CHASE,
        pixel_count=3,
        active_pixel_count=1,
        group_size=1,
    )

    assert len(steps) == 3
    assert tuple(step.frame.index(RGB(255, 0, 0)) for step in steps) == (0, 1, 2)


def test_groups_mode_includes_short_final_group() -> None:
    steps = build_diagnostic_steps(
        mode=DiagnosticMode.GROUPS,
        pixel_count=5,
        active_pixel_count=1,
        group_size=2,
    )

    assert len(steps) == 3
    assert steps[-1].frame == (
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 0),
        RGB(0, 0, 255),
    )


def test_ramp_mode_reaches_full_strip_once() -> None:
    steps = build_diagnostic_steps(
        mode=DiagnosticMode.RAMP,
        pixel_count=5,
        active_pixel_count=1,
        group_size=2,
    )

    assert len(steps) == 3
    assert [sum(pixel != RGB(0, 0, 0) for pixel in step.frame) for step in steps] == [2, 4, 5]


def test_hardware_parser_uses_safe_defaults() -> None:
    arguments = create_parser().parse_args([])

    assert arguments.mode is DiagnosticMode.CHANNELS
    assert arguments.pixel_count == 120
    assert arguments.active_pixel_count == 5
    assert arguments.group_size == 10
    assert arguments.brightness == 8
    assert arguments.allow_full_strip is False


def test_white_mode_requires_explicit_permission() -> None:
    with pytest.raises(ValueError, match="requires --allow-full-strip"):
        main(["--mode", "white"])
