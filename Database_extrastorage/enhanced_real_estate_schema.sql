-- Enhanced Real Estate Database Schema for PropSoch.com
-- Updated to include detailed room dimensions and specifications

Table users {
  user_id int [pk, increment]
  email varchar(255) [unique, not null]
  phone varchar(20) [unique]
  password_hash varchar(255) [not null]
  first_name varchar(100) [not null]
  last_name varchar(100) [not null]
  user_type varchar(20) [default: 'buyer', note: 'buyer, seller, agent, admin']
  is_verified boolean [default: false]
  created_at timestamp [default: `now()`]
  last_login timestamp
  profile_image_url varchar(500)
  is_active boolean [default: true]
}

Table developers {
  developer_id int [pk, increment]
  name varchar(255) [not null]
  established_year int
  description text
  logo_url varchar(500)
  website_url varchar(500)
  contact_email varchar(255)
  contact_phone varchar(20)
  address text
  total_projects int [default: 0]
  completed_projects int [default: 0]
  ongoing_projects int [default: 0]
  rating decimal(3,2) [default: 0.00]
  total_reviews int [default: 0]
  is_verified boolean [default: false]
  created_at timestamp [default: `now()`]
}

Table cities {
  city_id int [pk, increment]
  name varchar(100) [not null]
  state varchar(100) [not null]
  country varchar(100) [not null]
  latitude decimal(10,8)
  longitude decimal(11,8)
}

Table localities {
  locality_id int [pk, increment]
  city_id int [not null]
  name varchar(255) [not null]
  locality_type varchar(20) [default: 'locality', note: 'locality, micro_market, suburb']
  pincode varchar(10)
  latitude decimal(10,8)
  longitude decimal(11,8)
  description text
  created_at timestamp [default: `now()`]
}

Table projects {
  project_id int [pk, increment]
  developer_id int [not null]
  locality_id int [not null]
  name varchar(255) [not null]
  project_type varchar(20) [default: 'residential', note: 'residential, commercial, mixed']
  property_type varchar(20) [not null, note: 'apartment, villa, plot, office, retail']
  status varchar(30) [not null, note: 'under_construction, ready_to_move, new_launch, completed']
  
  // Project Details
  total_land_area decimal(10,2) [note: 'in acres']
  total_units int
  unit_density decimal(8,2) [note: 'units per acre']
  open_area_percentage decimal(5,2)
  park_area decimal(8,2) [note: 'in acres']
  clubhouse_area decimal(10,2) [note: 'in sq ft']
  
  // Pricing
  min_price decimal(15,2)
  max_price decimal(15,2)
  price_per_sqft decimal(10,2)
  currency varchar(10) [default: 'INR']
  
  // Timeline
  launch_date date
  possession_date date
  completion_date date
  
  // Location specifics
  address text
  latitude decimal(10,8)
  longitude decimal(11,8)
  approach_road_width decimal(8,2) [note: 'in meters']
  nearest_metro_distance decimal(8,2) [note: 'in km']
  airport_distance decimal(8,2) [note: 'in km']
  
  // RERA Details
  rera_number varchar(100)
  rera_website varchar(500)
  rera_status varchar(20) [default: 'approved', note: 'approved, pending, expired']
  
  // Content
  description text
  highlights text
  master_plan_url varchar(500)
  brochure_url varchar(500)
  
  // SEO and Status
  meta_title varchar(255)
  meta_description text
  is_active boolean [default: true]
  
  created_at timestamp [default: `now()`]
}

Table towers {
  tower_id int [pk, increment]
  project_id int [not null]
  tower_name varchar(100) [not null]
  tower_number varchar(50)
  total_floors int [not null]
  units_per_floor int [default: 0]
  total_units int [default: 0]
  tower_type varchar(20) [default: 'residential', note: 'residential, commercial, mixed']
  
  // Tower specifics
  construction_status varchar(30) [default: 'under_construction', note: 'under_construction, completed, ready_to_move']
  possession_date date
  height_meters decimal(8,2)
  
  // Facilities
  elevator_count int [default: 0]
  has_power_backup boolean [default: true]
  has_water_backup boolean [default: true]
  has_fire_safety boolean [default: true]
  
  // Positioning
  latitude decimal(10,8)
  longitude decimal(11,8)
  facing_direction varchar(20) [note: 'north, south, east, west, northeast, northwest, southeast, southwest']
  
  is_active boolean [default: true]
}

Table unit_types {
  unit_type_id int [pk, increment]
  project_id int [not null]
  type_name varchar(100) [not null, note: 'e.g., 3BHK, 4BHK+Maid, 1BHK+Study']
  bedrooms int [not null]
  bathrooms int [not null]

  // Room counts
  master_bedrooms int [default: 0]
  child_bedrooms int [default: 0]
  guest_bedrooms int [default: 0]
  study_rooms int [default: 0]
  living_rooms int [default: 1]
  dining_rooms int [default: 0]
  kitchens int [default: 1]
  utility_rooms int [default: 0]
  store_rooms int [default: 0]
  pooja_rooms int [default: 0]

  // Maid room details
  has_maid_room boolean [default: false]
  maid_room_area decimal(8,2) [note: 'in sq ft']
  has_maid_bathroom boolean [default: false]
  
  // Balcony details
  has_balcony boolean [default: true]
  balcony_count int [default: 0]
  total_balcony_area decimal(8,2) [note: 'in sq ft']
  
  // Additional areas
  has_terrace boolean [default: false]
  terrace_area decimal(8,2) [note: 'in sq ft']
  has_private_garden boolean [default: false]
  private_garden_area decimal(8,2) [note: 'in sq ft']

  // Area Details
  carpet_area decimal(10,2) [note: 'in sq ft']
  built_up_area decimal(10,2) [note: 'in sq ft']
  super_area decimal(10,2) [note: 'in sq ft']
  carpet_ratio decimal(5,2) [note: 'carpet area percentage']
  
  // Pricing
  base_price decimal(15,2)
  price_per_sqft decimal(10,2)
  
  // Layout specifications
  floor_plan_url varchar(500)
  floor_height decimal(5,2) [note: 'in meters']
  ceiling_height decimal(5,2) [note: 'in meters']
  facing_direction varchar(20) [note: 'north, south, east, west, northeast, northwest, southeast, southwest']
  
  // Door specifications
  main_door_type varchar(50) [note: 'wooden, steel, glass, etc.']
  main_door_width decimal(5,2) [note: 'in meters']
  main_door_height decimal(5,2) [note: 'in meters']
  bedroom_door_type varchar(50)
  bathroom_door_type varchar(50)
  
  // Window specifications
  window_type varchar(50) [note: 'sliding, casement, french, etc.']
  window_material varchar(50) [note: 'aluminum, upvc, wooden, etc.']

  // Availability
  total_units int [default: 0]
  available_units int [default: 0]
  sold_units int [default: 0]
  
  is_active boolean [default: true]
  created_at timestamp [default: `now()`]
}

-- Enhanced room details table with comprehensive specifications
Table unit_room_details {
  room_detail_id int [pk, increment]
  unit_type_id int [not null]
  room_type varchar(50) [not null, note: 'master_bedroom, child_bedroom, guest_bedroom, living_room, dining_room, kitchen, bathroom, balcony, study_room, utility_room, store_room, pooja_room, foyer, passage']
  room_name varchar(100) [note: 'Master Bedroom, Child Bedroom 1, Living Room, etc.']
  room_sequence int [default: 1, note: 'For multiple rooms of same type']
  
  // Dimensions (PRIMARY ENHANCEMENT)
  room_length decimal(8,2) [not null, note: 'in meters']
  room_width decimal(8,2) [not null, note: 'in meters']
  room_area decimal(8,2) [not null, note: 'in sq ft']
  
  // Shape and layout
  room_shape varchar(30) [default: 'rectangular', note: 'rectangular, square, l_shaped, irregular']
  
  // Room specific features
  has_attached_bathroom boolean [default: false]
  has_balcony_access boolean [default: false]
  has_wardrobe boolean [default: false]
  wardrobe_type varchar(50) [note: 'built-in, walk-in, modular']
  wardrobe_area decimal(6,2) [note: 'in sq ft']
  
  // Natural light and ventilation
  has_window boolean [default: true]
  window_count int [default: 1]
  window_total_area decimal(6,2) [note: 'in sq ft']
  natural_light_rating varchar(10) [default: 'good', note: 'excellent, good, average, poor']
  ventilation_rating varchar(10) [default: 'good', note: 'excellent, good, average, poor']
  
  // Doors and Windows specifications
  door_count int [default: 1]
  door_type varchar(50) [note: 'single, double, sliding, folding']
  door_material varchar(50) [note: 'wood, steel, glass, composite']
  door_width decimal(5,2) [note: 'in meters']
  door_height decimal(5,2) [note: 'in meters']
  
  window_type varchar(50) [note: 'sliding, casement, french, bay, fixed']
  window_material varchar(50) [note: 'aluminum, upvc, wooden, steel']
  window_width decimal(5,2) [note: 'in meters']
  window_height decimal(5,2) [note: 'in meters']
  
  // Electrical specifications
  electrical_points int [default: 0]
  fan_points int [default: 0]
  ac_points int [default: 0]
  light_points int [default: 0]
  
  // Flooring and ceiling
  flooring_type varchar(50) [note: 'marble, vitrified_tiles, ceramic, wooden, granite']
  flooring_brand varchar(100)
  ceiling_type varchar(50) [note: 'pop, gypsum, concrete, wooden']
  ceiling_height decimal(5,2) [note: 'in meters']
  
  // Fixtures (for bathrooms and kitchen)
  has_geyser_provision boolean [default: false]
  has_exhaust_fan boolean [default: false]
  has_chimney_provision boolean [default: false]
  
  // Privacy and position
  privacy_level varchar(20) [default: 'private', note: 'private, semi_private, open']
  position_in_unit varchar(30) [note: 'front, back, side, central, corner']
  
  created_at timestamp [default: `now()`]
}

-- New table for detailed balcony specifications
Table balcony_details {
  balcony_id int [pk, increment]
  unit_type_id int [not null]
  balcony_name varchar(100) [note: 'Master Bedroom Balcony, Living Room Balcony, etc.']
  balcony_sequence int [default: 1, note: 'For multiple balconies']
  
  // Dimensions
  balcony_length decimal(8,2) [not null, note: 'in meters']
  balcony_width decimal(8,2) [not null, note: 'in meters']
  balcony_area decimal(8,2) [not null, note: 'in sq ft']
  
  // Access and connection
  connected_room varchar(50) [note: 'master_bedroom, living_room, dining_room, kitchen']
  access_type varchar(30) [default: 'sliding_door', note: 'sliding_door, french_door, open']
  
  // Features
  balcony_type varchar(30) [default: 'regular', note: 'regular, utility, sit_out, deck']
  has_provision_for_washing_machine boolean [default: false]
  has_provision_for_drying boolean [default: true]
  has_safety_grill boolean [default: true]
  
  // View and orientation
  facing_direction varchar(20) [note: 'north, south, east, west, northeast, northwest, southeast, southwest']
  view_description text [note: 'garden view, road view, park view, etc.']
  floor_level varchar(20) [note: 'ground, podium, tower, terrace']
  
  created_at timestamp [default: `now()`]
}

Table property_units {
  unit_id int [pk, increment]
  project_id int [not null]
  unit_type_id int [not null]
  tower_id int [not null]
  unit_number varchar(50) [not null]
  floor_number int [not null]

  unit_position varchar(20) [note: 'corner, middle, end']
  wing varchar(10) [note: 'A, B, C, etc.']
  
  // Specific unit details
  carpet_area decimal(10,2)
  built_up_area decimal(10,2)
  super_area decimal(10,2)
  
  has_corner_unit boolean [default: false]
  has_extra_balcony boolean [default: false]
  has_servant_quarter boolean [default: false]
  
  // Pricing
  unit_price decimal(15,2)
  price_per_sqft decimal(10,2)
  maintenance_charge decimal(10,2)
  
  // Status
  status varchar(20) [default: 'available', note: 'available, sold, blocked, reserved']
  possession_date date
  
  // Premium/Discount
  premium_percentage decimal(5,2) [default: 0.00]
  discount_percentage decimal(5,2) [default: 0.00]
  
  // Specific details
  actual_facing_direction varchar(20)
  view_description text [note: 'garden view, road view, etc.']

  is_active boolean [default: true]
  created_at timestamp [default: `now()`]
}

-- Enhanced door and window specifications
Table door_window_specs {
  spec_id int [pk, increment]
  unit_type_id int [not null]
  item_type varchar(20) [not null, note: 'door, window']
  location varchar(100) [not null, note: 'main_entrance, master_bedroom, kitchen, etc.']
  
  // Physical specifications
  width decimal(5,2) [note: 'in meters']
  height decimal(5,2) [note: 'in meters']
  thickness decimal(5,2) [note: 'in mm']
  
  // Material and finish
  material varchar(50) [note: 'wood, steel, aluminum, upvc, glass']
  finish varchar(50) [note: 'polished, painted, laminated, etc.']
  brand varchar(100)
  grade varchar(50) [note: 'premium, standard, economy']
  
  // Features
  is_security_door boolean [default: false]
  has_grill boolean [default: false]
  opening_type varchar(30) [note: 'sliding, hinged, folding, casement']
  
  // Hardware
  lock_type varchar(50) [note: 'mortise, cylindrical, smart_lock']
  handle_type varchar(50)
  handle_material varchar(30)
  
  // Glass specifications (for windows)
  glass_type varchar(50) [note: 'clear, tinted, frosted, laminated']
  glass_thickness decimal(4,2) [note: 'in mm']
  
  created_at timestamp [default: `now()`]
}

Table amenities {
  amenity_id int [pk, increment]
  name varchar(100) [not null]
  category varchar(20) [not null, note: 'lifestyle, sports, natural, security, connectivity, wellness']
  icon_url varchar(500)
  description text
  is_rare boolean [default: false, note: 'for rare amenities']
  is_active boolean [default: true]
  created_at timestamp [default: `now()`]
}

Table project_amenities {
  project_id int [not null]
  amenity_id int [not null]
  is_available boolean [default: true]
  description text
  area_size decimal(10,2) [note: 'in sq ft']
  capacity int [note: 'number of people/units it can accommodate']
  operating_hours varchar(100)
  created_at timestamp [default: `now()`]
  
  Indexes {
    (project_id, amenity_id) [pk]
  }
}

Table project_media {
  media_id int [pk, increment]
  project_id int [not null]
  media_type varchar(20) [not null, note: 'image, video, virtual_tour, floor_plan, master_plan']
  media_url varchar(500) [not null]
  thumbnail_url varchar(500)
  title varchar(255)
  description text
  media_category varchar(20) [default: 'exterior', note: 'exterior, interior, amenities, views, construction, location']
  is_active boolean [default: true]
  created_at timestamp [default: `now()`]
}

Table approvals {
  approval_id int [pk, increment]
  name varchar(255) [not null]
  description text
  is_mandatory boolean [default: true]
  category varchar(20) [default: 'legal', note: 'legal, environmental, fire_safety, structural, other']
  created_at timestamp [default: `now()`]
}

Table project_approvals {
  project_id int [not null]
  approval_id int [not null]
  status varchar(20) [default: 'pending', note: 'pending, approved, rejected, expired']
  approval_number varchar(100)
  approval_date date
  expiry_date date
  issuing_authority varchar(255)
  document_url varchar(500)
  notes text
  created_at timestamp [default: `now()`]
  
  Indexes {
    (project_id, approval_id) [pk]
  }
}

Table project_documents {
  document_id int [pk, increment]
  project_id int [not null]
  document_type varchar(20) [not null, note: 'brochure, price_list, floor_plan, master_plan, legal_doc, approval, other']
  title varchar(255) [not null]
  description text
  file_url varchar(500) [not null]
  file_size bigint [note: 'in bytes']
  file_type varchar(50)
  is_public boolean [default: true]
  download_count int [default: 0]
  created_at timestamp [default: `now()`]
}

Table user_interests {
  interest_id int [pk, increment]
  user_id int [not null]
  project_id int
  unit_type_id int
  interest_type varchar(20) [not null, note: 'enquiry, site_visit, callback, brochure_download, price_quote']
  
  // Contact preferences
  preferred_contact_method varchar(20) [default: 'phone', note: 'phone, email, whatsapp']
  preferred_contact_time varchar(20) [default: 'anytime', note: 'morning, afternoon, evening, anytime']
  
  // Requirements
  budget_min decimal(15,2)
  budget_max decimal(15,2)
  preferred_floors text [note: 'comma separated']
  specific_requirements text
  
  // Status
  status varchar(30) [default: 'new', note: 'new, contacted, site_visit_scheduled, site_visit_done, negotiating, closed_won, closed_lost']
  assigned_to int [note: 'agent user_id']
  
  notes text
  created_at timestamp [default: `now()`]
}

Table reviews {
  review_id int [pk, increment]
  project_id int
  developer_id int
  user_id int [not null]
  rating int [not null, note: 'CHECK (rating >= 1 AND rating <= 5)']
  title varchar(255)
  review_text text
  pros text
  cons text
  
  // Review categories
  construction_quality_rating int [note: 'CHECK (1-5)']
  amenities_rating int [note: 'CHECK (1-5)']
  location_rating int [note: 'CHECK (1-5)']
  value_for_money_rating int [note: 'CHECK (1-5)']
  
  is_verified boolean [default: false]
  created_at timestamp [default: `now()`]
}

Table search_logs {
  search_id int [pk, increment]
  user_id int
  search_query varchar(500)
  filters_applied text [note: 'JSON format']
  results_count int
  clicked_project_id int
  search_timestamp timestamp [default: `now()`]
  session_id varchar(255)
  ip_address varchar(45)
}

Table property_comparisons {
  comparison_id int [pk, increment]
  user_id int
  project_ids text [not null, note: 'JSON Array of project IDs']
  comparison_parameters text [note: 'JSON - Parameters used for comparison']
  session_id varchar(255)
  created_at timestamp [default: `now()`]
}

Table notifications {
  notification_id int [pk, increment]
  user_id int [not null]
  type varchar(20) [not null, note: 'price_change, new_project, similar_property, reminder, update, promotional']
  title varchar(255) [not null]
  message text [not null]
  related_project_id int
  is_read boolean [default: false]
  is_sent boolean [default: false]
  delivery_method varchar(20) [default: 'in_app', note: 'email, sms, push, in_app']
  created_at timestamp [default: `now()`]
  read_at timestamp
}

Table price_history {
  price_history_id int [pk, increment]
  project_id int
  unit_type_id int
  old_price decimal(15,2)
  new_price decimal(15,2)
  old_price_per_sqft decimal(10,2)
  new_price_per_sqft decimal(10,2)
  change_percentage decimal(5,2)
  change_reason varchar(255)
  effective_date date
  created_at timestamp [default: `now()`]
}

// RELATIONSHIPS
Ref: "developers"."developer_id" < "projects"."developer_id"
Ref: "localities"."locality_id" < "projects"."locality_id"
Ref: "cities"."city_id" < "localities"."city_id"
Ref: "projects"."project_id" < "unit_types"."project_id"
Ref: "projects"."project_id" < "property_units"."project_id"
Ref: "unit_types"."unit_type_id" < "property_units"."unit_type_id"
Ref: "projects"."project_id" < "towers"."project_id"
Ref: "towers"."tower_id" < "property_units"."tower_id"
Ref: "unit_types"."unit_type_id" < "unit_room_details"."unit_type_id"
Ref: "unit_types"."unit_type_id" < "balcony_details"."unit_type_id"
Ref: "unit_types"."unit_type_id" < "door_window_specs"."unit_type_id"
Ref: "projects"."project_id" < "project_amenities"."project_id"
Ref: "amenities"."amenity_id" < "project_amenities"."amenity_id"
Ref: "projects"."project_id" < "project_media"."project_id"
Ref: "projects"."project_id" < "project_approvals"."project_id"
Ref: "approvals"."approval_id" < "project_approvals"."approval_id"
Ref: "projects"."project_id" < "project_documents"."project_id"
Ref: "users"."user_id" < "user_interests"."user_id"
Ref: "projects"."project_id" < "user_interests"."project_id"
Ref: "unit_types"."unit_type_id" < "user_interests"."unit_type_id"
Ref: "projects"."project_id" < "reviews"."project_id"
Ref: "developers"."developer_id" < "reviews"."developer_id"
Ref: "users"."user_id" < "reviews"."user_id"
Ref: "users"."user_id" < "search_logs"."user_id"
Ref: "users"."user_id" < "property_comparisons"."user_id"
Ref: "users"."user_id" < "notifications"."user_id"
Ref: "projects"."project_id" < "price_history"."project_id"
Ref: "unit_types"."unit_type_id" < "price_history"."unit_type_id"