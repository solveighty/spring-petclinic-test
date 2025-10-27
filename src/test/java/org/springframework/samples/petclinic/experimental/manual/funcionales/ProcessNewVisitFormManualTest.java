package org.springframework.samples.petclinic.owner;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
class ProcessNewVisitFormManualTest {

	@Autowired
	private MockMvc mockMvc;

	// Vista creada exitosamente retorna redirección
	@Test
	void shouldRedirectWhenVisitCreatedSuccessfully() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/13/visits/new").param("date", "2025-10-26")
				.param("description", "Monthly pet check-up"))
			.andExpect(status().is3xxRedirection())
			.andExpect(view().name("redirect:/owners/{ownerId}"));
	}

	// Fecha inválida retorna formulario con error
	@Test
	void shouldReturnFormWhenInvalidDate() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/13/visits/new").param("date", "2025-10-2")
				.param("description", "Monthly pet check-up"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdateVisitForm"));
	}

	// Descripción vacía retorna formulario con error
	@Test
	void shouldReturnFormWhenDescriptionIsEmpty() throws Exception {
		mockMvc.perform(post("/owners/10/pets/13/visits/new").param("date", "2025-10-26").param("description", ""))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdateVisitForm"));
	}

	// Owner no existe retorna Internal Server Error o 500
	@Test
	void shouldReturnServerErrorWhenOwnerDoesNotExist() throws Exception {
		mockMvc
			.perform(post("/owners/99/pets/13/visits/new").param("date", "2025-10-26")
				.param("description", "Monthly pet check-up"))
			.andExpect(status().isInternalServerError());
	}

	// Pet que no existe retorna Internal Server Error o 500
	@Test
	void shouldReturnServerErrorWhenPetDoesNotExist() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/999/visits/new").param("date", "2025-10-26")
				.param("description", "Monthly pet check-up"))
			.andExpect(status().isInternalServerError());
	}

	// Cuando se envía con fecha vacia retorna formulario con error
	@Test
	void shouldReturnFormWhenDateIsEmpty() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/13/visits/new").param("date", "")
				.param("description", "Monthly pet check-up"))
			.andExpect(status().is3xxRedirection())
			.andExpect(view().name("pets/createOrUpdateVisitForm"));
	}

	// Cuando se envía con descripción vacía retorna formulario con error
	@Test
	void shouldReturnFormWhenDescriptionIsMissing() throws Exception {
		mockMvc.perform(post("/owners/10/pets/13/visits/new").param("date", "2025-10-26"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdateVisitForm"));
	}

}
