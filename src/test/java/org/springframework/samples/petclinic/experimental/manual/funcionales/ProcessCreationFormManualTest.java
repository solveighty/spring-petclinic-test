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
class ProcessCreationFormManualTest {

	@Autowired
	private MockMvc mockMvc;

	// Retorna redireccion cuando la mascota se crea exitosamente
	@Test
	void shouldRedirectWhenPetCreatedSuccessfully() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "Bol").param("birthDate", "2023-01-15").param("type.id", "1"))
			.andExpect(status().is3xxRedirection())
			.andExpect(view().name("redirect:/owners/{ownerId}"));
	}

	// Retorna redirección cuando la mascota se crea exitosamente con número en el nombre
	@Test
	void shouldRedirectWhenPetCreatedSuccessfullyWithNumberInName() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/new").param("name", "Bol123")
				.param("birthDate", "2023-01-15")
				.param("type.id", "1"))
			.andExpect(status().is3xxRedirection())
			.andExpect(view().name("redirect:/owners/{ownerId}"));
	}

	// Retorna formulario cuando el nombre de la mascota ya existe
	@Test
	void shouldReturnFormWhenDuplicateName() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "Bol").param("birthDate", "2023-01-15").param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdatePetForm"))
			.andExpect(model().attributeHasFieldErrorCode("pet", "name", "duplicate"));
	}

	// Retorna formulario cuando la fecha de nacimiento es invalida
	@Test
	void shouldReturnFormWhenInvalidDate() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "Kito").param("birthDate", "2025-01-4").param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdatePetForm"))
			.andExpect(model().attributeHasFieldErrorCode("pet", "birthDate", "typeMismatch"));
	}

	// Retorna Internal Server Error cuando el tipo de mascota es invalido
	@Test
	void shouldReturnServerErrorWhenInvalidType() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/new").param("name", "Loro")
				.param("birthDate", "2023-01-15")
				.param("type.id", "-1"))
			.andExpect(status().isInternalServerError());
	}

	// Retorna Internal Server Error cuando el tipo de mascota no existe
	@Test
	void shouldReturnServerErrorWhenTypeDoesNotExist() throws Exception {
		mockMvc
			.perform(post("/owners/10/pets/new").param("name", "Loro")
				.param("birthDate", "2023-01-15")
				.param("type.id", "8"))
			.andExpect(status().isInternalServerError());
	}

	// En caso de que el nombre este vacio, retorna el formulario
	@Test
	void shouldReturnFormWhenNameIsEmpty() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "").param("birthDate", "2023-01-15").param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdatePetForm"))
			.andExpect(model().attributeHasFieldErrors("pet", "name"));
	}

	// En caso de que la fecha de nacimiento este vacia, retorna el formulario
	@Test
	void shouldReturnFormWhenBirthDateIsEmpty() throws Exception {
		mockMvc.perform(post("/owners/10/pets/new").param("name", "Kito").param("birthDate", "").param("type.id", "1"))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdatePetForm"))
			.andExpect(model().attributeHasFieldErrors("pet", "birthDate"));
	}

	// En caso de que el tipo de mascota este vacio, retorna el formulario
	@Test
	void shouldReturnFormWhenTypeIsEmpty() throws Exception {
		mockMvc.perform(
				post("/owners/10/pets/new").param("name", "Kito").param("birthDate", "2023-01-15").param("type.id", ""))
			.andExpect(status().isOk())
			.andExpect(view().name("pets/createOrUpdatePetForm"))
			.andExpect(model().attributeHasFieldErrors("pet", "type"));
	}

	// Retorna Internal Server Error cuando el owner no existe
	@Test
	void shouldReturnServerErrorWhenOwnerDoesNotExist() throws Exception {
		mockMvc
			.perform(post("/owners/30/pets/new").param("name", "Kito")
				.param("birthDate", "2023-01-15")
				.param("type.id", "1"))
			.andExpect(status().isInternalServerError());
	}

}
