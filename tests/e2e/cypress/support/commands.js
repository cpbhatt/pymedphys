// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add('compute', () => {
  cy.get("#ReportStatus").should("be.visible")
  cy.get("#ReportStatus").should("not.be.visible")
})

Cypress.Commands.add('textMatch', (label, length, result) => {
  cy.get(`.stMarkdown p:contains(${label})`).should("have.length", length).find('code').each((el) => {
    return cy.wrap(el).should("have.text", result)
  })
})

Cypress.Commands.add('start', () => {
  cy.visit("http://localhost:8501/");
  cy.compute()
  cy.get(".decoration").invoke("css", "display", "none");
})