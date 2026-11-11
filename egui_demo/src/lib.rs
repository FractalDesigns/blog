use eframe::egui;
use wasm_bindgen::prelude::*;

#[derive(PartialEq, Clone, Copy)]
enum AppTab {
    Widgets,
    Graphics,
    Diagnostics,
}

#[derive(PartialEq, Clone, Copy)]
enum Mood {
    Fast,
    Smooth,
    Chill,
}

pub struct DemoApp {
    // Widgets tab
    name: String,
    counter: i32,
    slider_val: f32,
    checkbox_enabled: bool,
    radio_choice: Mood,
    dropdown_selected: String,
    picked_color: [f32; 3],

    // Graphics tab
    circle_radius: f32,
    wave_frequency: f32,
    animate_wave: bool,
    time: f32,

    // Navigation
    current_tab: AppTab,
}

impl Default for DemoApp {
    fn default() -> Self {
        Self {
            name: "Sphinx Reader".to_owned(),
            counter: 12,
            slider_val: 45.0,
            checkbox_enabled: true,
            radio_choice: Mood::Smooth,
            dropdown_selected: "Rust + WebAssembly".to_owned(),
            picked_color: [0.06, 0.72, 0.51], // #10b981 (Lumina Emerald)

            circle_radius: 50.0,
            wave_frequency: 2.0,
            animate_wave: true,
            time: 0.0,

            current_tab: AppTab::Widgets,
        }
    }
}

impl DemoApp {
    pub fn new(_cc: &eframe::CreationContext<'_>) -> Self {
        Self::default()
    }
}

impl eframe::App for DemoApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if self.animate_wave {
            self.time += ctx.input(|i| i.stable_dt).min(0.1);
            ctx.request_repaint();
        }

        egui::CentralPanel::default().show(ctx, |ui| {
            // Top Bar
            ui.horizontal(|ui| {
                ui.heading("🦀 egui Showcase");
                ui.label(concat!("v", env!("CARGO_PKG_VERSION")));

                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                    egui::widgets::global_theme_preference_buttons(ui);
                });
            });

            ui.separator();

            // Tab bar
            ui.horizontal(|ui| {
                ui.selectable_value(&mut self.current_tab, AppTab::Widgets, "🎛️ Interactive Controls");
                ui.selectable_value(&mut self.current_tab, AppTab::Graphics, "🎨 Live WebGL Canvas");
                ui.selectable_value(&mut self.current_tab, AppTab::Diagnostics, "📊 System & Metrics");
            });

            ui.separator();

            match self.current_tab {
                AppTab::Widgets => self.render_widgets_tab(ui),
                AppTab::Graphics => self.render_graphics_tab(ui),
                AppTab::Diagnostics => self.render_diagnostics_tab(ui, ctx),
            }
        });
    }
}

impl DemoApp {
    fn render_widgets_tab(&mut self, ui: &mut egui::Ui) {
        egui::ScrollArea::vertical().show(ui, |ui| {
            ui.columns(2, |columns| {
                // Left Column: Inputs & Controls
                columns[0].group(|ui| {
                    ui.label(egui::RichText::new("User Inputs").strong());

                    ui.horizontal(|ui| {
                        ui.label("Name:");
                        ui.text_edit_singleline(&mut self.name);
                    });

                    ui.add_space(4.0);
                    ui.horizontal(|ui| {
                        ui.label("Speed:");
                        ui.add(egui::Slider::new(&mut self.slider_val, 0.0..=100.0).suffix(" km/h"));
                    });

                    ui.add_space(4.0);
                    ui.checkbox(&mut self.checkbox_enabled, "Enable active indicators");

                    ui.add_space(4.0);
                    ui.horizontal(|ui| {
                        ui.label("Mode:");
                        ui.radio_value(&mut self.radio_choice, Mood::Fast, "Fast");
                        ui.radio_value(&mut self.radio_choice, Mood::Smooth, "Smooth");
                        ui.radio_value(&mut self.radio_choice, Mood::Chill, "Chill");
                    });

                    ui.add_space(4.0);
                    ui.horizontal(|ui| {
                        ui.label("Tech Stack:");
                        egui::ComboBox::from_id_salt("tech_combo")
                            .selected_text(&self.dropdown_selected)
                            .show_ui(ui, |ui| {
                                ui.selectable_value(&mut self.dropdown_selected, "Rust + WebAssembly".into(), "Rust + WebAssembly");
                                ui.selectable_value(&mut self.dropdown_selected, "Sphinx + Lumina".into(), "Sphinx + Lumina");
                                ui.selectable_value(&mut self.dropdown_selected, "egui Immediate GUI".into(), "egui Immediate GUI");
                            });
                    });

                    ui.add_space(4.0);
                    ui.horizontal(|ui| {
                        ui.label("Accent Color:");
                        ui.color_edit_button_rgb(&mut self.picked_color);
                    });
                });

                // Right Column: State & Interactive Actions
                columns[1].group(|ui| {
                    ui.label(egui::RichText::new("Interactive Actions").strong());

                    ui.horizontal(|ui| {
                        if ui.button("➖ Subtract").clicked() {
                            self.counter -= 1;
                        }
                        ui.label(egui::RichText::new(format!("Count: {}", self.counter)).strong().size(16.0));
                        if ui.button("➕ Add").clicked() {
                            self.counter += 1;
                        }
                        if ui.button("↺ Reset").clicked() {
                            self.counter = 0;
                        }
                    });

                    ui.add_space(8.0);
                    let progress = ((self.counter.abs() % 50) as f32) / 50.0;
                    ui.add(egui::ProgressBar::new(progress).show_percentage().animate(self.checkbox_enabled));

                    ui.add_space(12.0);
                    ui.separator();
                    ui.add_space(4.0);

                    let c = self.picked_color;
                    let text_color = egui::Color32::from_rgb((c[0] * 255.0) as u8, (c[1] * 255.0) as u8, (c[2] * 255.0) as u8);

                    ui.colored_label(
                        text_color,
                        format!("👋 Hello, {}!", if self.name.is_empty() { "friend" } else { &self.name }),
                    );
                    ui.label(format!("• Slider: {:.1}", self.slider_val));
                    ui.label(format!("• Selection: {}", self.dropdown_selected));
                    ui.label(format!(
                        "• Mode: {}",
                        match self.radio_choice {
                            Mood::Fast => "⚡ Fast",
                            Mood::Smooth => "🌊 Smooth",
                            Mood::Chill => "☕ Chill",
                        }
                    ));
                });
            });
        });
    }

    fn render_graphics_tab(&mut self, ui: &mut egui::Ui) {
        ui.horizontal(|ui| {
            ui.add(egui::Slider::new(&mut self.circle_radius, 10.0..=120.0).text("Radius"));
            ui.add(egui::Slider::new(&mut self.wave_frequency, 0.5..=10.0).text("Wave Frequency"));
            ui.checkbox(&mut self.animate_wave, "Animate");
        });

        ui.add_space(8.0);

        // Custom 2D painter area
        let (response, painter) = ui.allocate_painter(
            egui::Vec2::new(ui.available_width(), 260.0),
            egui::Sense::drag(),
        );

        let rect = response.rect;
        painter.rect_filled(rect, 8.0, egui::Color32::from_rgb(24, 24, 27));

        // Draw animated sine wave
        let points = 120;
        let mut wave_points = Vec::with_capacity(points);
        for i in 0..points {
            let t = (i as f32) / (points as f32);
            let x = rect.left() + t * rect.width();
            let y = rect.center().y + (t * self.wave_frequency * std::f32::consts::TAU + self.time * 3.0).sin() * 50.0;
            wave_points.push(egui::Pos2::new(x, y));
        }

        let stroke_color = egui::Color32::from_rgb(
            (self.picked_color[0] * 255.0) as u8,
            (self.picked_color[1] * 255.0) as u8,
            (self.picked_color[2] * 255.0) as u8,
        );
        painter.add(egui::Shape::line(
            wave_points,
            egui::Stroke::new(2.5_f32, stroke_color),
        ));

        // Draw interactive circle centered in canvas
        let circle_center = rect.center();
        painter.circle_filled(
            circle_center,
            self.circle_radius,
            egui::Color32::from_rgba_unmultiplied(
                (self.picked_color[0] * 255.0) as u8,
                (self.picked_color[1] * 255.0) as u8,
                (self.picked_color[2] * 255.0) as u8,
                140,
            ),
        );
        painter.circle_stroke(
            circle_center,
            self.circle_radius,
            egui::Stroke::new(2.0_f32, egui::Color32::WHITE),
        );

        painter.text(
            rect.center(),
            egui::Align2::CENTER_CENTER,
            "Drag & Adjust Sliders",
            egui::FontId::proportional(14.0),
            egui::Color32::WHITE,
        );
    }

    fn render_diagnostics_tab(&mut self, ui: &mut egui::Ui, ctx: &egui::Context) {
        ui.group(|ui| {
            ui.label(egui::RichText::new("Runtime Environment").strong());
            ui.label("• Target Architecture: wasm32-unknown-unknown");
            ui.label("• Rendering Backend: glow (WebGL 2.0 / 1.0)");
            ui.label(format!("• Pixels per point: {:.2}", ctx.pixels_per_point()));
            ui.label(format!("• Viewport size: {:.0} x {:.0} pt", ui.available_width(), ui.available_height()));
            ui.label(format!("• Animation running: {}", self.animate_wave));
            ui.label(format!("• Elapsed app time: {:.1}s", self.time));
        });

        ui.add_space(8.0);
        ui.label(egui::RichText::new("About egui").strong());
        ui.label("egui is an immediate mode GUI library for Rust. Immediate mode means every frame the UI is recreated from scratch, resulting in zero out-of-sync state bugs and instant reactivity.");
    }
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
pub struct WebHandle {
    runner: eframe::WebRunner,
}

#[cfg(target_arch = "wasm32")]
#[wasm_bindgen]
impl WebHandle {
    #[wasm_bindgen(constructor)]
    #[allow(clippy::new_without_default)]
    pub fn new() -> Self {
        eframe::WebLogger::init(log::LevelFilter::Debug).ok();
        Self {
            runner: eframe::WebRunner::new(),
        }
    }

    #[wasm_bindgen]
    pub async fn start(&self, canvas_id: &str) -> Result<(), wasm_bindgen::JsValue> {
        use wasm_bindgen::JsCast;

        console_error_panic_hook::set_once();

        let window = web_sys::window().ok_or_else(|| wasm_bindgen::JsValue::from_str("No window found"))?;
        let document = window
            .document()
            .ok_or_else(|| wasm_bindgen::JsValue::from_str("No document found"))?;
        let element = document
            .get_element_by_id(canvas_id)
            .ok_or_else(|| wasm_bindgen::JsValue::from_str(&format!("Canvas '{canvas_id}' not found")))?;
        let canvas: web_sys::HtmlCanvasElement = element
            .dyn_into::<web_sys::HtmlCanvasElement>()
            .map_err(|_| wasm_bindgen::JsValue::from_str("Element is not a canvas"))?;

        self.runner
            .start(
                canvas,
                eframe::WebOptions::default(),
                Box::new(|cc| Ok(Box::new(DemoApp::new(cc)))),
            )
            .await
    }
}
